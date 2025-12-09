"""
Student analyzer module that processes student answers and performance.
"""
from typing import List, Dict, Any
from datetime import datetime
from models import (
    Question,
    StudentAttempt,
    StudentPerformance,
    DifficultyLevel
)


class StudentAnalyzer:
    """
    Analyzes student answers and updates performance metrics.
    Uses labeled data (attempts, correctness, difficulty, topic tags).
    """
    
    def __init__(self):
        """Initialize the analyzer."""
        self.students: Dict[str, StudentPerformance] = {}
    
    def get_or_create_student(self, student_id: str) -> StudentPerformance:
        """Get existing student performance or create new one."""
        if student_id not in self.students:
            self.students[student_id] = StudentPerformance(student_id=student_id)
        return self.students[student_id]
    
    def analyze_answer(
        self,
        student_id: str,
        question: Question,
        student_answer: str,
        time_taken_seconds: int
    ) -> StudentAttempt:
        """
        Analyze a student's answer to a question.
        
        Args:
            student_id: Unique identifier for the student
            question: The question that was answered
            student_answer: The student's submitted answer
            time_taken_seconds: Time taken to answer in seconds
            
        Returns:
            StudentAttempt object with analysis results
        """
        # Determine if answer is correct (case-insensitive comparison)
        is_correct = self._check_answer_correctness(
            student_answer,
            question.correct_answer
        )
        
        # Create attempt record with labeled data
        attempt = StudentAttempt(
            question_id=question.id,
            student_answer=student_answer,
            is_correct=is_correct,
            timestamp=datetime.now(),
            time_taken_seconds=time_taken_seconds,
            topic=question.topic,
            difficulty=question.difficulty
        )
        
        # Update student performance
        performance = self.get_or_create_student(student_id)
        performance.add_attempt(attempt)
        
        return attempt
    
    def _check_answer_correctness(
        self,
        student_answer: str,
        correct_answer: str
    ) -> bool:
        """
        Check if the student's answer is correct.
        
        Args:
            student_answer: The student's submitted answer
            correct_answer: The correct answer
            
        Returns:
            True if answer is correct, False otherwise
        """
        # Normalize answers for comparison (lowercase, strip whitespace)
        normalized_student = student_answer.strip().lower()
        normalized_correct = correct_answer.strip().lower()
        
        return normalized_student == normalized_correct
    
    def get_performance_summary(self, student_id: str) -> Dict[str, Any]:
        """
        Get a comprehensive performance summary for a student.
        
        Args:
            student_id: Unique identifier for the student
            
        Returns:
            Dictionary containing performance metrics
        """
        performance = self.get_or_create_student(student_id)
        
        # Calculate accuracy by difficulty
        difficulty_stats = {
            "easy": performance.get_difficulty_accuracy(DifficultyLevel.EASY),
            "medium": performance.get_difficulty_accuracy(DifficultyLevel.MEDIUM),
            "hard": performance.get_difficulty_accuracy(DifficultyLevel.HARD)
        }
        
        # Get unique topics
        topics = list(set(attempt.topic for attempt in performance.attempts))
        topic_stats = {
            topic: performance.get_topic_accuracy(topic)
            for topic in topics
        }
        
        # Calculate average time per attempt
        if performance.attempts:
            avg_time = sum(a.time_taken_seconds for a in performance.attempts) / len(performance.attempts)
        else:
            avg_time = 0
        
        return {
            "student_id": student_id,
            "total_attempts": performance.total_attempts,
            "correct_attempts": performance.correct_attempts,
            "overall_accuracy": performance.get_accuracy(),
            "difficulty_accuracy": difficulty_stats,
            "topic_accuracy": topic_stats,
            "average_time_seconds": avg_time,
            "recent_attempts": [
                {
                    "question_id": a.question_id,
                    "topic": a.topic,
                    "difficulty": a.difficulty.name,
                    "is_correct": a.is_correct,
                    "time_taken": a.time_taken_seconds
                }
                for a in performance.get_recent_attempts(5)
            ]
        }
    
    def get_topic_insights(self, student_id: str, topic: str) -> Dict[str, Any]:
        """
        Get detailed insights for a specific topic.
        
        Args:
            student_id: Unique identifier for the student
            topic: The topic to analyze
            
        Returns:
            Dictionary containing topic-specific insights
        """
        performance = self.get_or_create_student(student_id)
        topic_attempts = [a for a in performance.attempts if a.topic == topic]
        
        if not topic_attempts:
            return {
                "topic": topic,
                "attempts": 0,
                "accuracy": 0.0,
                "message": f"No attempts yet for {topic}"
            }
        
        correct = sum(1 for a in topic_attempts if a.is_correct)
        accuracy = (correct / len(topic_attempts)) * 100
        
        # Get difficulty breakdown
        difficulty_breakdown = {}
        for difficulty in DifficultyLevel:
            diff_attempts = [a for a in topic_attempts if a.difficulty == difficulty]
            if diff_attempts:
                diff_correct = sum(1 for a in diff_attempts if a.is_correct)
                difficulty_breakdown[difficulty.name] = {
                    "attempts": len(diff_attempts),
                    "correct": diff_correct,
                    "accuracy": (diff_correct / len(diff_attempts)) * 100
                }
        
        return {
            "topic": topic,
            "attempts": len(topic_attempts),
            "correct": correct,
            "accuracy": accuracy,
            "difficulty_breakdown": difficulty_breakdown,
            "needs_review": accuracy < 70.0
        }
