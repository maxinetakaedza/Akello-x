from collections import defaultdict
from datetime import datetime, timedelta
from dateutil import parser
from typing import Dict, Any, List, Optional

# Prototype thresholds; tweak as needed
DEFAULT_CONFIG = {
    'correct_streak_for_up': 3,
    'wrong_streak_for_down': 2,
    'avoid_days_threshold': 7,   # days without attempts => considered avoided
    'xp_per_correct': 10,
    'weekly_xp_threshold': 200,
}

class RuleEngine:
    def __init__(self, datastore, config=None):
        self.ds = datastore
        self.config = config or DEFAULT_CONFIG
        # ephemeral per-student per-topic streaks kept in memory for fast decisions
        # {student_id: {topic: {'correct_streak': int, 'wrong_streak': int, 'last_attempt_ts': str}}}
        self.streaks: Dict[str, Dict[str, Dict[str, Any]]] = defaultdict(lambda: defaultdict(lambda: {
            'correct_streak': 0,
            'wrong_streak': 0,
            'last_attempt_ts': None
        }))

    def process_attempt(self, student_id: str, attempt: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry: record attempt, update profile & streaks, apply rules, return decision.
        attempt keys required: question_id, topic, difficulty (easy/medium/hard), correct (bool), time_spent_seconds
        """

        # 1) record attempt in datastore
        attempt = self.ds.record_attempt(student_id, attempt)

        # 2) update streaks
        topic = attempt['topic']
        s = self.streaks[student_id][topic]
        if attempt['correct']:
            s['correct_streak'] += 1
            s['wrong_streak'] = 0
        else:
            s['wrong_streak'] += 1
            s['correct_streak'] = 0
        s['last_attempt_ts'] = attempt['ts']

        # 3) difficulty adjustment
        difficulty_action = None
        if s['correct_streak'] >= self.config['correct_streak_for_up']:
            difficulty_action = 'increase'
            # reset streak to avoid repeated increases
            s['correct_streak'] = 0
        elif s['wrong_streak'] >= self.config['wrong_streak_for_down']:
            difficulty_action = 'decrease'
            s['wrong_streak'] = 0

        # 4) weakness detection: mark topic weak if repeated fails overall (simple heuristic)
        profile = self.ds.get_profile(student_id)
        topic_attempts = [a for a in self.ds.get_attempts(student_id) if a['topic'] == topic]
        recent_fail_rate = None
        if topic_attempts:
            last_n = topic_attempts[-10:]  # look at last up-to 10 attempts
            failures = sum(1 for a in last_n if not a['correct'])
            recent_fail_rate = failures / len(last_n)
        is_weak = False
        if recent_fail_rate is not None and recent_fail_rate >= 0.6 and len(topic_attempts) >= 3:
            is_weak = True
            profile['weak_topics'][topic] = profile['weak_topics'].get(topic, 0) + 1  # counter
        # If student avoids a topic (no attempts in threshold days)
        avoided_topics = []
        now = datetime.utcnow()
        for qtopic, ts in profile.get('last_seen', {}).items():
            try:
                last = parser.isoparse(ts)
            except Exception:
                continue
            if (now - last).days >= self.config['avoid_days_threshold']:
                avoided_topics.append(qtopic)

        # 5) XP & gamification
        gained_xp = self.config['xp_per_correct'] if attempt['correct'] else 0
        profile['xp'] = profile.get('xp', 0) + gained_xp
        level_up = False
        if profile['xp'] >= self.config['weekly_xp_threshold']:
            profile['level'] = profile.get('level', 1) + 1
            profile['xp'] = profile['xp'] - self.config['weekly_xp_threshold']
            level_up = True

        # 6) micro-lesson suggestion rules
        micro_lesson = None
        soft_quiz = None
        if is_weak and attempt['difficulty'] == 'easy':
            micro_lesson = {
                'topic': topic,
                'reason': 'weak detected and current difficulty easy',
                'resource_type': 'micro_lesson',
                'length_minutes': 5
            }
        if topic in avoided_topics:
            soft_quiz = {
                'topic': topic,
                'reason': 'topic avoided (no recent activity)',
                'resource_type': 'micro_lesson_plus_soft_quiz',
                'length_minutes': 7
            }

        # 7) Decide next question selection hint (this is a prototype selection hint)
        next_action = {}
        if micro_lesson:
            next_action['action'] = 'show_micro_lesson'
            next_action['payload'] = micro_lesson
        elif soft_quiz:
            next_action['action'] = 'offer_micro_lesson_and_soft_quiz'
            next_action['payload'] = soft_quiz
        elif difficulty_action == 'increase':
            next_action['action'] = 'increase_difficulty'
            next_action['payload'] = {'topic': topic, 'new_difficulty_suggestion': self._higher_difficulty(attempt['difficulty'])}
        elif difficulty_action == 'decrease':
            next_action['action'] = 'decrease_difficulty'
            next_action['payload'] = {'topic': topic, 'new_difficulty_suggestion': self._lower_difficulty(attempt['difficulty'])}
        else:
            # default: recommend next questions in same topic with same difficulty, plus a small spacer
            next_action['action'] = 'next_questions'
            next_action['payload'] = {
                'topic': topic,
                'difficulty': attempt['difficulty'],
                'suggested_count': 3
            }

        # 8) Weekly mission & summary
        weekly_mission = None
        if profile.get('weak_topics'):
            weekly_mission = {
                'mission': 'Focus on weak topics',
                'topics': list(profile['weak_topics'].keys())
            }

        # assemble decision object
        decision = {
            'student_id': student_id,
            'topic': topic,
            'attempt': attempt,
            'next_action': next_action,
            'xp_gained': gained_xp,
            'level_up': level_up,
            'weekly_mission': weekly_mission
        }

        return decision

    def _higher_difficulty(self, d: str) -> str:
        order = ['easy', 'medium', 'hard']
        try:
            idx = order.index(d)
            return order[min(len(order)-1, idx+1)]
        except ValueError:
            return d

    def _lower_difficulty(self, d: str) -> str:
        order = ['easy', 'medium', 'hard']
        try:
            idx = order.index(d)
            return order[max(0, idx-1)]
        except ValueError:
            return d

    # -----------------
    # Supervised helper
    # -----------------
    def induce_candidate_rules(self, student_id_list: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Very simple heuristic to propose candidate rules from historical data:
        - For each student/topic/difficulty we look for sequences where failing N hard => later success after medium revision.
        - If a positive effect (improvement rate) is strong, propose a rule "fail X hard -> revisit medium".
        This is a prototype — treat results as suggestions for human review/A-B tests.
        """
        candidates = []
        # gather all students if not provided
        student_ids = student_id_list or list(self.ds.attempts.keys())
        for sid in student_ids:
            attempts = self.ds.get_attempts(sid)
            # group by topic
            by_topic = defaultdict(list)
            for a in attempts:
                by_topic[a['topic']].append(a)
            for topic, alist in by_topic.items():
                # look for patterns in sliding windows
                for i in range(len(alist)-2):
                    first = alist[i]
                    second = alist[i+1]
                    third = alist[i+2]
                    # simple heuristic: failed 2 hard in row, then medium correct => candidate
                    if first['difficulty'] == 'hard' and second['difficulty'] == 'hard' and not first['correct'] and not second['correct']:
                        if third['difficulty'] == 'medium' and third['correct']:
                            candidates.append({
                                'rule_proposal': "fail_2_hard_then_medium_help",
                                'topic': topic,
                                'evidence_example': [first, second, third],
                                'reason': 'observed user improved after medium-level revision'
                            })
        # deduplicate proposals by topic
        unique = {}
        for c in candidates:
            key = (c['rule_proposal'], c['topic'])
            if key not in unique:
                unique[key] = c
        return list(unique.values())
