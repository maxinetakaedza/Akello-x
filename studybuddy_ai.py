"""
StudyBuddy AI - First AI system that tracks performance over time.
Supports both batch (free) and real-time (premium) analysis.
"""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict
from models import StudentPerformance, DifficultyLevel
from extended_models import (
    UserTier, TrendDirection, SubjectStrength, WeeklyMission,
    MistakeExplanation, StudyBuddyReport
)


class StudyBuddyAI:
    """
    AI #1 - StudyBuddy AI
    
    Tracks performance over time in Study Sessions and Quizzes.
    Generates strength/weakness scores, recommendations, and explanations.
    """
    
    def __init__(self):
        """Initialize StudyBuddy AI."""
        self.student_data: Dict[str, StudentPerformance] = {}
        self.last_report: Dict[str, datetime] = {}
    
    def analyze_performance(
        self,
        student_id: str,
        performance: StudentPerformance,
        tier: UserTier = UserTier.FREE
    ) -> StudyBuddyReport:
        """
        Analyze student performance and generate report.
        
        For FREE tier: Weekly batch analysis
        For PREMIUM tier: Real-time analysis available anytime
        
        Args:
            student_id: Student identifier
            performance: Student's performance data
            tier: User subscription tier
            
        Returns:
            StudyBuddyReport with analysis and recommendations
        """
        # Check if analysis is allowed based on tier
        if tier == UserTier.FREE:
            if not self._should_generate_weekly_report(student_id):
                # Return last report or empty report
                return self._get_cached_report(student_id)
        
        # Generate comprehensive analysis
        report = StudyBuddyReport(
            student_id=student_id,
            report_date=datetime.now(),
            tier=tier
        )
        
        # Analyze each subject
        subjects = self._get_subjects_from_performance(performance)
        for subject in subjects:
            strength = self._analyze_subject_strength(performance, subject)
            report.subject_strengths.append(strength)
        
        # Calculate overall metrics
        report.overall_confidence = self._calculate_overall_confidence(
            report.subject_strengths
        )
        report.overall_trend = self._calculate_overall_trend(performance)
        
        # Topic difficulty mapping
        report.topic_difficulty_map = self._create_topic_difficulty_map(performance)
        
        # Generate recommendations
        report.recommended_quizzes = self._recommend_quizzes(
            report.subject_strengths, tier
        )
        report.weekly_mission = self._create_weekly_mission(
            report.subject_strengths, performance
        )
        
        # Generate explanations
        report.mistake_explanations = self._generate_mistake_explanations(
            performance, tier
        )
        
        # Extract pain points for Career AI
        report.pain_points = self._extract_pain_points(report.subject_strengths)
        
        # Cache report
        self._cache_report(student_id, report)
        
        return report
    
    def _should_generate_weekly_report(self, student_id: str) -> bool:
        """Check if it's time for weekly report (free tier)."""
        if student_id not in self.last_report:
            return True
        
        last_report_date = self.last_report[student_id]
        days_since_last = (datetime.now() - last_report_date).days
        
        return days_since_last >= 7
    
    def _get_cached_report(self, student_id: str) -> StudyBuddyReport:
        """Get cached report or create empty one."""
        # In a real system, this would fetch from database
        return StudyBuddyReport(
            student_id=student_id,
            report_date=datetime.now(),
            tier=UserTier.FREE
        )
    
    def _cache_report(self, student_id: str, report: StudyBuddyReport):
        """Cache the generated report."""
        self.last_report[student_id] = report.report_date
    
    def _get_subjects_from_performance(
        self, performance: StudentPerformance
    ) -> List[str]:
        """Extract unique subjects from attempts."""
        subjects = set()
        for attempt in performance.attempts:
            subjects.add(attempt.topic)
        return list(subjects)
    
    def _analyze_subject_strength(
        self,
        performance: StudentPerformance,
        subject: str
    ) -> SubjectStrength:
        """
        Analyze strength/weakness for a specific subject.
        
        Returns SubjectStrength with scores and analysis.
        """
        subject_attempts = [
            a for a in performance.attempts if a.topic == subject
        ]
        
        if not subject_attempts:
            return SubjectStrength(
                subject=subject,
                strength_score=0.0,
                weakness_score=100.0,
                confidence_score=0.0,
                trend=TrendDirection.STABLE
            )
        
        # Calculate accuracy
        correct = sum(1 for a in subject_attempts if a.is_correct)
        accuracy = (correct / len(subject_attempts)) * 100
        
        # Strength score (based on accuracy)
        strength_score = accuracy
        weakness_score = 100 - accuracy
        
        # Confidence score (accuracy + consistency)
        recent_accuracy = self._get_recent_accuracy(subject_attempts[-5:])
        confidence_score = (accuracy + recent_accuracy) / 2
        
        # Trend analysis
        trend = self._calculate_trend(subject_attempts)
        
        # Identify pain points
        pain_points = self._identify_pain_points(subject_attempts, subject)
        
        # Determine mastery level
        mastery = self._determine_mastery_level(accuracy, len(subject_attempts))
        
        return SubjectStrength(
            subject=subject,
            strength_score=strength_score,
            weakness_score=weakness_score,
            confidence_score=confidence_score,
            trend=trend,
            pain_points=pain_points,
            mastery_level=mastery
        )
    
    def _get_recent_accuracy(self, attempts: List) -> float:
        """Calculate accuracy for recent attempts."""
        if not attempts:
            return 0.0
        correct = sum(1 for a in attempts if a.is_correct)
        return (correct / len(attempts)) * 100
    
    def _calculate_trend(self, attempts: List) -> TrendDirection:
        """Calculate performance trend."""
        if len(attempts) < 4:
            return TrendDirection.STABLE
        
        # Compare first half vs second half
        mid = len(attempts) // 2
        first_half_accuracy = self._get_recent_accuracy(attempts[:mid])
        second_half_accuracy = self._get_recent_accuracy(attempts[mid:])
        
        diff = second_half_accuracy - first_half_accuracy
        
        if diff > 10:
            return TrendDirection.IMPROVING
        elif diff < -10:
            return TrendDirection.DECLINING
        else:
            return TrendDirection.STABLE
    
    def _identify_pain_points(self, attempts: List, subject: str) -> List[str]:
        """Identify specific pain points in a subject."""
        pain_points = []
        
        # Check difficulty struggles
        difficulty_stats = defaultdict(lambda: {"correct": 0, "total": 0})
        for attempt in attempts:
            difficulty_stats[attempt.difficulty.name]["total"] += 1
            if attempt.is_correct:
                difficulty_stats[attempt.difficulty.name]["correct"] += 1
        
        for difficulty, stats in difficulty_stats.items():
            if stats["total"] > 0:
                accuracy = (stats["correct"] / stats["total"]) * 100
                if accuracy < 50:
                    pain_points.append(f"{difficulty} questions in {subject}")
        
        # Check for recent consecutive failures
        consecutive_wrong = 0
        for attempt in reversed(attempts[-5:]):
            if not attempt.is_correct:
                consecutive_wrong += 1
            else:
                break
        
        if consecutive_wrong >= 3:
            pain_points.append(f"Recent struggles with {subject}")
        
        return pain_points
    
    def _determine_mastery_level(self, accuracy: float, attempts_count: int) -> str:
        """Determine mastery level based on accuracy and experience."""
        if attempts_count < 5:
            return "beginner"
        
        if accuracy >= 85:
            return "advanced"
        elif accuracy >= 65:
            return "intermediate"
        else:
            return "beginner"
    
    def _calculate_overall_confidence(
        self, subject_strengths: List[SubjectStrength]
    ) -> float:
        """Calculate overall confidence across all subjects."""
        if not subject_strengths:
            return 0.0
        
        total_confidence = sum(s.confidence_score for s in subject_strengths)
        return total_confidence / len(subject_strengths)
    
    def _calculate_overall_trend(
        self, performance: StudentPerformance
    ) -> TrendDirection:
        """Calculate overall performance trend."""
        if len(performance.attempts) < 10:
            return TrendDirection.STABLE
        
        # Compare first 50% vs last 50%
        mid = len(performance.attempts) // 2
        first_half = performance.attempts[:mid]
        second_half = performance.attempts[mid:]
        
        first_accuracy = self._get_recent_accuracy(first_half)
        second_accuracy = self._get_recent_accuracy(second_half)
        
        diff = second_accuracy - first_accuracy
        
        if diff > 10:
            return TrendDirection.IMPROVING
        elif diff < -10:
            return TrendDirection.DECLINING
        else:
            return TrendDirection.STABLE
    
    def _create_topic_difficulty_map(
        self, performance: StudentPerformance
    ) -> Dict[str, float]:
        """Map topics to their perceived difficulty for the student."""
        topic_map = {}
        
        topics = set(a.topic for a in performance.attempts)
        for topic in topics:
            topic_attempts = [a for a in performance.attempts if a.topic == topic]
            accuracy = self._get_recent_accuracy(topic_attempts)
            # Difficulty is inverse of accuracy
            difficulty = 100 - accuracy
            topic_map[topic] = difficulty
        
        return topic_map
    
    def _recommend_quizzes(
        self, subject_strengths: List[SubjectStrength], tier: UserTier
    ) -> List[str]:
        """Recommend quizzes based on weaknesses."""
        recommendations = []
        
        # Find weakest subjects
        weak_subjects = [
            s for s in subject_strengths 
            if s.weakness_score > 50
        ]
        
        # Sort by weakness
        weak_subjects.sort(key=lambda s: s.weakness_score, reverse=True)
        
        # Recommend quizzes
        limit = 5 if tier == UserTier.PREMIUM else 3
        for subject in weak_subjects[:limit]:
            recommendations.append(f"{subject.subject} Review Quiz")
        
        return recommendations
    
    def _create_weekly_mission(
        self,
        subject_strengths: List[SubjectStrength],
        performance: StudentPerformance
    ) -> Optional[WeeklyMission]:
        """Create a weekly fix-your-weakness mission."""
        if not subject_strengths:
            return None
        
        # Find the weakest subject
        weakest = max(subject_strengths, key=lambda s: s.weakness_score)
        
        # Create mission
        mission = WeeklyMission(
            mission_id=f"mission_{datetime.now().strftime('%Y%m%d')}",
            subject=weakest.subject,
            title=f"Master {weakest.subject}",
            description=f"Focus on improving your {weakest.subject} skills this week",
            target_topics=[weakest.subject],
            difficulty_focus="easy" if weakest.mastery_level == "beginner" else "medium",
            estimated_time_minutes=30
        )
        
        return mission
    
    def _generate_mistake_explanations(
        self, performance: StudentPerformance, tier: UserTier
    ) -> List[MistakeExplanation]:
        """Generate explanations for mistakes."""
        explanations = []
        
        # Get recent incorrect attempts
        incorrect_attempts = [
            a for a in performance.attempts[-10:] if not a.is_correct
        ]
        
        limit = 10 if tier == UserTier.PREMIUM else 3
        
        for attempt in incorrect_attempts[:limit]:
            basic_exp = f"The correct answer was different from your response."
            deep_exp = None
            
            if tier == UserTier.PREMIUM:
                deep_exp = (
                    f"You answered '{attempt.student_answer}' but the correct answer "
                    f"requires understanding of {attempt.topic} concepts. "
                    f"This appears to be a {attempt.difficulty.name} level question. "
                    f"Review the fundamentals of {attempt.topic} to improve."
                )
            
            explanation = MistakeExplanation(
                question_id=attempt.question_id,
                student_answer=attempt.student_answer,
                correct_answer="[See question for correct answer]",
                basic_explanation=basic_exp,
                deep_explanation=deep_exp,
                related_concepts=[attempt.topic],
                remediation_steps=[
                    f"Review {attempt.topic} basics",
                    f"Practice more {attempt.difficulty.name} questions"
                ]
            )
            explanations.append(explanation)
        
        return explanations
    
    def _extract_pain_points(
        self, subject_strengths: List[SubjectStrength]
    ) -> List[str]:
        """Extract pain points for Career AI."""
        pain_points = []
        
        for subject in subject_strengths:
            pain_points.extend(subject.pain_points)
        
        return pain_points
