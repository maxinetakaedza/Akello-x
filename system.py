"""
Main system that integrates the analyzer and rule engine.
"""
from typing import Optional
from models import Question, DifficultyLevel, NextAction
from analyzer import StudentAnalyzer
from rule_engine import RuleEngine


class StudentPerformanceSystem:
    """
    Main system that combines analysis and decision-making.
    This is the primary interface for the rule-based supervised system.
    """
    
    def __init__(self):
        """Initialize the system with analyzer and rule engine."""
        self.analyzer = StudentAnalyzer()
        self.rule_engine = RuleEngine()
    
    def process_answer(
        self,
        student_id: str,
        question: Question,
        student_answer: str,
        time_taken_seconds: int,
        current_topic: str
    ) -> dict:
        """
        Process a student's answer and decide what to show next.
        
        Args:
            student_id: Unique identifier for the student
            question: The question that was answered
            student_answer: The student's submitted answer
            time_taken_seconds: Time taken to answer
            current_topic: The current topic being studied
            
        Returns:
            Dictionary containing analysis results and next action
        """
        # Analyze the answer
        attempt = self.analyzer.analyze_answer(
            student_id=student_id,
            question=question,
            student_answer=student_answer,
            time_taken_seconds=time_taken_seconds
        )
        
        # Get student performance
        performance = self.analyzer.get_or_create_student(student_id)
        
        # Use rule engine to decide next action
        decision = self.rule_engine.decide_next_action(performance, current_topic)
        
        # Build response
        response = {
            "attempt": {
                "is_correct": attempt.is_correct,
                "correct_answer": question.correct_answer,
                "explanation": question.explanation,
                "time_taken": attempt.time_taken_seconds
            },
            "performance": {
                "total_attempts": performance.total_attempts,
                "overall_accuracy": performance.get_accuracy(),
                "topic_accuracy": performance.get_topic_accuracy(current_topic)
            },
            "next_action": {
                "action": decision.next_action.value,
                "reason": decision.reason,
                "topic": decision.topic,
                "difficulty": decision.difficulty.name if decision.difficulty else None,
                "message": decision.message
            }
        }
        
        return response
    
    def get_student_summary(self, student_id: str) -> dict:
        """Get comprehensive performance summary for a student."""
        return self.analyzer.get_performance_summary(student_id)
    
    def get_next_action_for_student(
        self,
        student_id: str,
        current_topic: str
    ) -> dict:
        """
        Get next action recommendation without processing an answer.
        Useful for starting a new session or continuing practice.
        
        Args:
            student_id: Unique identifier for the student
            current_topic: The topic to practice
            
        Returns:
            Dictionary with next action recommendation
        """
        performance = self.analyzer.get_or_create_student(student_id)
        decision = self.rule_engine.decide_next_action(performance, current_topic)
        
        return {
            "action": decision.next_action.value,
            "reason": decision.reason,
            "topic": decision.topic,
            "difficulty": decision.difficulty.name if decision.difficulty else None,
            "message": decision.message,
            "performance": {
                "total_attempts": performance.total_attempts,
                "overall_accuracy": performance.get_accuracy(),
                "topic_accuracy": performance.get_topic_accuracy(current_topic)
            }
        }


# Example usage function
def create_sample_questions():
    """Create sample questions for demonstration."""
    questions = [
        Question(
            id="q1",
            topic="algebra",
            difficulty=DifficultyLevel.EASY,
            content="What is 2 + 2?",
            correct_answer="4",
            explanation="Basic addition: 2 + 2 = 4"
        ),
        Question(
            id="q2",
            topic="algebra",
            difficulty=DifficultyLevel.EASY,
            content="What is 5 * 3?",
            correct_answer="15",
            explanation="Multiplication: 5 * 3 = 15"
        ),
        Question(
            id="q3",
            topic="algebra",
            difficulty=DifficultyLevel.MEDIUM,
            content="Solve for x: 2x + 4 = 10",
            correct_answer="3",
            explanation="Subtract 4 from both sides: 2x = 6, then divide by 2: x = 3"
        ),
        Question(
            id="q4",
            topic="algebra",
            difficulty=DifficultyLevel.HARD,
            content="Solve for x: x^2 - 5x + 6 = 0",
            correct_answer="2 or 3",
            explanation="Factor: (x-2)(x-3) = 0, so x = 2 or x = 3"
        ),
        Question(
            id="q5",
            topic="geometry",
            difficulty=DifficultyLevel.EASY,
            content="How many sides does a triangle have?",
            correct_answer="3",
            explanation="A triangle has 3 sides by definition"
        ),
        Question(
            id="q6",
            topic="geometry",
            difficulty=DifficultyLevel.MEDIUM,
            content="What is the area of a rectangle with length 5 and width 3?",
            correct_answer="15",
            explanation="Area = length * width = 5 * 3 = 15"
        ),
    ]
    return questions


if __name__ == "__main__":
    # Example demonstration
    print("=" * 60)
    print("Rule-Based Student Performance Analysis System")
    print("=" * 60)
    
    # Create system and sample questions
    system = StudentPerformanceSystem()
    questions = create_sample_questions()
    
    student_id = "student_001"
    topic = "algebra"
    
    # Simulate student answering questions
    print(f"\nStudent: {student_id}, Topic: {topic}\n")
    
    # First question
    print("Question 1: What is 2 + 2?")
    result = system.process_answer(
        student_id=student_id,
        question=questions[0],
        student_answer="4",
        time_taken_seconds=5,
        current_topic=topic
    )
    print(f"Correct: {result['attempt']['is_correct']}")
    print(f"Next Action: {result['next_action']['action']}")
    print(f"Message: {result['next_action']['message']}\n")
    
    # Second question
    print("Question 2: What is 5 * 3?")
    result = system.process_answer(
        student_id=student_id,
        question=questions[1],
        student_answer="15",
        time_taken_seconds=8,
        current_topic=topic
    )
    print(f"Correct: {result['attempt']['is_correct']}")
    print(f"Next Action: {result['next_action']['action']}")
    print(f"Message: {result['next_action']['message']}\n")
    
    # Get summary
    summary = system.get_student_summary(student_id)
    print("=" * 60)
    print("Student Performance Summary")
    print("=" * 60)
    print(f"Total Attempts: {summary['total_attempts']}")
    print(f"Correct Attempts: {summary['correct_attempts']}")
    print(f"Overall Accuracy: {summary['overall_accuracy']:.1f}%")
    print(f"Topic Accuracy: {summary['topic_accuracy']}")
