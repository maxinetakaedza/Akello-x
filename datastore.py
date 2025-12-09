# Simple in-memory datastore for prototype (replace with DB for production)
from collections import defaultdict
from datetime import datetime
from typing import Dict, List

class DataStore:
    def __init__(self):
        # student_id -> list of attempts (most recent last)
        self.attempts: Dict[str, List[dict]] = defaultdict(list)
        # student profiles
        self.profiles: Dict[str, dict] = {}
        # question bank
        self.questions: Dict[str, dict] = {}

    def add_question_bank(self, questions: list):
        for q in questions:
            self.questions[q['id']] = q

    def record_attempt(self, student_id: str, attempt: dict):
        attempt = dict(attempt)
        attempt['ts'] = datetime.utcnow().isoformat()
        self.attempts[student_id].append(attempt)
        # ensure profile exists
        self.profiles.setdefault(student_id, {
            'xp': 0,
            'level': 1,
            'weak_topics': {},
            'last_seen': {},
        })
        self.profiles[student_id]['last_seen'][attempt['topic']] = attempt['ts']
        return attempt

    def get_attempts(self, student_id: str):
        return list(self.attempts.get(student_id, []))

    def get_profile(self, student_id: str):
        return self.profiles.setdefault(student_id, {
            'xp': 0,
            'level': 1,
            'weak_topics': {},
            'last_seen': {},
        })
