"""
Rule-based decision engine for determining what to show next to students.
"""
from typing import List, Optional
from models import (
    StudentPerformance,
    StudentAttempt,
    DifficultyLevel,
    NextAction,
    DecisionResult
)


class RuleEngine:
    """
    Rule-based supervised system that uses explicit if-then rules to decide
    what to show next (questions, lessons, or feedback).
    """
    
    # Configurable thresholds
    LOW_ACCURACY_THRESHOLD = 50.0
    MEDIUM_ACCURACY_THRESHOLD = 75.0
    HIGH_ACCURACY_THRESHOLD = 90.0
    RECENT_ATTEMPTS_COUNT = 5
    CONSECUTIVE_INCORRECT_THRESHOLD = 3
    
    def __init__(self):
        """Initialize the rule engine."""
        pass
    
    def decide_next_action(
        self,
        performance: StudentPerformance,
        current_topic: str
    ) -> DecisionResult:
        """
        Main decision-making method using rule-based logic.
        
        Args:
            performance: Student's performance data
            current_topic: The current topic being studied
            
        Returns:
            DecisionResult with the next action to take
        """
        # Rule 1: If student has no attempts, start with an easy question
        if performance.total_attempts == 0:
            return DecisionResult(
                next_action=NextAction.QUESTION,
                reason="First question - starting with easy difficulty",
                topic=current_topic,
                difficulty=DifficultyLevel.EASY,
                message="Welcome! Let's start with a warm-up question."
            )
        
        # Get recent performance data
        recent_attempts = performance.get_recent_attempts(self.RECENT_ATTEMPTS_COUNT)
        topic_accuracy = performance.get_topic_accuracy(current_topic)
        overall_accuracy = performance.get_accuracy()
        
        # Rule 2: If student has consecutive incorrect answers, show lesson
        consecutive_incorrect = self._check_consecutive_incorrect(recent_attempts)
        if consecutive_incorrect >= self.CONSECUTIVE_INCORRECT_THRESHOLD:
            return DecisionResult(
                next_action=NextAction.LESSON,
                reason=f"Struggled with {consecutive_incorrect} consecutive questions",
                topic=current_topic,
                message=f"Let's review the {current_topic} topic to strengthen your understanding."
            )
        
        # Rule 3: If topic accuracy is low, provide feedback and lesson
        if topic_accuracy < self.LOW_ACCURACY_THRESHOLD and performance.total_attempts >= 3:
            return DecisionResult(
                next_action=NextAction.FEEDBACK,
                reason=f"Low topic accuracy ({topic_accuracy:.1f}%)",
                topic=current_topic,
                message=f"Your accuracy in {current_topic} is {topic_accuracy:.1f}%. "
                        f"Let's review key concepts before continuing."
            )
        
        # Rule 4: If recent performance is poor but overall is okay, give targeted feedback
        recent_accuracy = self._calculate_recent_accuracy(recent_attempts)
        if recent_accuracy < self.LOW_ACCURACY_THRESHOLD and overall_accuracy >= self.MEDIUM_ACCURACY_THRESHOLD:
            return DecisionResult(
                next_action=NextAction.FEEDBACK,
                reason=f"Recent decline in performance ({recent_accuracy:.1f}%)",
                topic=current_topic,
                message="Your recent answers need improvement. Let's review what went wrong."
            )
        
        # Rule 5: If performing well on easy questions, increase difficulty
        easy_accuracy = performance.get_difficulty_accuracy(DifficultyLevel.EASY)
        if easy_accuracy >= self.HIGH_ACCURACY_THRESHOLD:
            recent_difficulty = self._get_recent_difficulty(recent_attempts)
            if recent_difficulty == DifficultyLevel.EASY:
                return DecisionResult(
                    next_action=NextAction.QUESTION,
                    reason=f"Mastered easy questions ({easy_accuracy:.1f}% accuracy)",
                    topic=current_topic,
                    difficulty=DifficultyLevel.MEDIUM,
                    message="Great job! Let's try a medium difficulty question."
                )
        
        # Rule 6: If performing well on medium questions, try hard
        medium_accuracy = performance.get_difficulty_accuracy(DifficultyLevel.MEDIUM)
        if medium_accuracy >= self.HIGH_ACCURACY_THRESHOLD:
            recent_difficulty = self._get_recent_difficulty(recent_attempts)
            if recent_difficulty == DifficultyLevel.MEDIUM:
                return DecisionResult(
                    next_action=NextAction.QUESTION,
                    reason=f"Mastered medium questions ({medium_accuracy:.1f}% accuracy)",
                    topic=current_topic,
                    difficulty=DifficultyLevel.HARD,
                    message="Excellent! You're ready for a challenging question."
                )
        
        # Rule 7: If struggling with hard questions, drop to medium
        hard_accuracy = performance.get_difficulty_accuracy(DifficultyLevel.HARD)
        if hard_accuracy < self.LOW_ACCURACY_THRESHOLD:
            recent_difficulty = self._get_recent_difficulty(recent_attempts)
            if recent_difficulty == DifficultyLevel.HARD:
                return DecisionResult(
                    next_action=NextAction.QUESTION,
                    reason=f"Struggling with hard questions ({hard_accuracy:.1f}% accuracy)",
                    topic=current_topic,
                    difficulty=DifficultyLevel.MEDIUM,
                    message="Let's practice with medium difficulty questions to build confidence."
                )
        
        # Rule 8: If overall accuracy is good, continue with same difficulty
        if overall_accuracy >= self.MEDIUM_ACCURACY_THRESHOLD:
            recent_difficulty = self._get_recent_difficulty(recent_attempts)
            return DecisionResult(
                next_action=NextAction.QUESTION,
                reason=f"Good performance ({overall_accuracy:.1f}% accuracy)",
                topic=current_topic,
                difficulty=recent_difficulty or DifficultyLevel.MEDIUM,
                message="Keep up the good work!"
            )
        
        # Default rule: Continue with appropriate difficulty based on performance
        difficulty = self._determine_difficulty_from_accuracy(topic_accuracy)
        return DecisionResult(
            next_action=NextAction.QUESTION,
            reason=f"Topic accuracy: {topic_accuracy:.1f}%",
            topic=current_topic,
            difficulty=difficulty,
            message="Let's continue practicing."
        )
    
    def _check_consecutive_incorrect(self, attempts: List[StudentAttempt]) -> int:
        """Count consecutive incorrect answers from the end."""
        count = 0
        for attempt in reversed(attempts):
            if not attempt.is_correct:
                count += 1
            else:
                break
        return count
    
    def _calculate_recent_accuracy(self, attempts: List[StudentAttempt]) -> float:
        """Calculate accuracy from recent attempts."""
        if not attempts:
            return 0.0
        correct = sum(1 for a in attempts if a.is_correct)
        return (correct / len(attempts)) * 100
    
    def _get_recent_difficulty(self, attempts: List[StudentAttempt]) -> Optional[DifficultyLevel]:
        """Get the difficulty level of the most recent attempt."""
        if not attempts:
            return None
        return attempts[-1].difficulty
    
    def _determine_difficulty_from_accuracy(self, accuracy: float) -> DifficultyLevel:
        """Determine appropriate difficulty based on accuracy."""
        if accuracy >= self.HIGH_ACCURACY_THRESHOLD:
            return DifficultyLevel.HARD
        elif accuracy >= self.MEDIUM_ACCURACY_THRESHOLD:
            return DifficultyLevel.MEDIUM
        else:
            return DifficultyLevel.EASY
