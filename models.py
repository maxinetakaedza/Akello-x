"""
Data models for the rule-based student performance analysis system.
"""
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class DifficultyLevel(Enum):
    """Difficulty levels for questions."""
    EASY = 1
    MEDIUM = 2
    HARD = 3


class NextAction(Enum):
    """Possible next actions to show the student."""
    QUESTION = "question"
    LESSON = "lesson"
    FEEDBACK = "feedback"


@dataclass
class Question:
    """Represents a question in the system."""
    id: str
    topic: str
    difficulty: DifficultyLevel
    content: str
    correct_answer: str
    explanation: Optional[str] = None


@dataclass
class StudentAttempt:
    """Represents a student's attempt at answering a question."""
    question_id: str
    student_answer: str
    is_correct: bool
    timestamp: datetime
    time_taken_seconds: int
    topic: str
    difficulty: DifficultyLevel


@dataclass
class StudentPerformance:
    """Tracks overall student performance."""
    student_id: str
    attempts: List[StudentAttempt] = field(default_factory=list)
    total_attempts: int = 0
    correct_attempts: int = 0
    
    def add_attempt(self, attempt: StudentAttempt):
        """Add a new attempt and update statistics."""
        self.attempts.append(attempt)
        self.total_attempts += 1
        if attempt.is_correct:
            self.correct_attempts += 1
    
    def get_accuracy(self) -> float:
        """Calculate overall accuracy percentage."""
        if self.total_attempts == 0:
            return 0.0
        return (self.correct_attempts / self.total_attempts) * 100
    
    def get_topic_accuracy(self, topic: str) -> float:
        """Calculate accuracy for a specific topic."""
        topic_attempts = [a for a in self.attempts if a.topic == topic]
        if not topic_attempts:
            return 0.0
        correct = sum(1 for a in topic_attempts if a.is_correct)
        return (correct / len(topic_attempts)) * 100
    
    def get_recent_attempts(self, count: int = 5) -> List[StudentAttempt]:
        """Get the most recent attempts."""
        return self.attempts[-count:] if len(self.attempts) >= count else self.attempts
    
    def get_difficulty_accuracy(self, difficulty: DifficultyLevel) -> float:
        """Calculate accuracy for a specific difficulty level."""
        difficulty_attempts = [a for a in self.attempts if a.difficulty == difficulty]
        if not difficulty_attempts:
            return 0.0
        correct = sum(1 for a in difficulty_attempts if a.is_correct)
        return (correct / len(difficulty_attempts)) * 100


@dataclass
class DecisionResult:
    """Result of the decision-making process."""
    next_action: NextAction
    reason: str
    topic: Optional[str] = None
    difficulty: Optional[DifficultyLevel] = None
    message: Optional[str] = None
