"""
Unit tests for the rule-based student performance analysis system.
"""
import unittest
from datetime import datetime
from models import (
    Question,
    StudentAttempt,
    StudentPerformance,
    DifficultyLevel,
    NextAction,
    DecisionResult
)
from analyzer import StudentAnalyzer
from rule_engine import RuleEngine
from system import StudentPerformanceSystem, create_sample_questions


class TestModels(unittest.TestCase):
    """Test data models."""
    
    def test_student_performance_initialization(self):
        """Test StudentPerformance initialization."""
        perf = StudentPerformance(student_id="test_001")
        self.assertEqual(perf.student_id, "test_001")
        self.assertEqual(perf.total_attempts, 0)
        self.assertEqual(perf.correct_attempts, 0)
        self.assertEqual(len(perf.attempts), 0)
    
    def test_add_attempt(self):
        """Test adding attempts to student performance."""
        perf = StudentPerformance(student_id="test_001")
        attempt = StudentAttempt(
            question_id="q1",
            student_answer="4",
            is_correct=True,
            timestamp=datetime.now(),
            time_taken_seconds=5,
            topic="math",
            difficulty=DifficultyLevel.EASY
        )
        perf.add_attempt(attempt)
        
        self.assertEqual(perf.total_attempts, 1)
        self.assertEqual(perf.correct_attempts, 1)
        self.assertEqual(len(perf.attempts), 1)
    
    def test_accuracy_calculation(self):
        """Test accuracy calculation."""
        perf = StudentPerformance(student_id="test_001")
        
        # Add correct attempt
        perf.add_attempt(StudentAttempt(
            question_id="q1", student_answer="4", is_correct=True,
            timestamp=datetime.now(), time_taken_seconds=5,
            topic="math", difficulty=DifficultyLevel.EASY
        ))
        
        # Add incorrect attempt
        perf.add_attempt(StudentAttempt(
            question_id="q2", student_answer="5", is_correct=False,
            timestamp=datetime.now(), time_taken_seconds=10,
            topic="math", difficulty=DifficultyLevel.EASY
        ))
        
        self.assertEqual(perf.get_accuracy(), 50.0)
    
    def test_topic_accuracy(self):
        """Test topic-specific accuracy."""
        perf = StudentPerformance(student_id="test_001")
        
        # Add math attempts
        perf.add_attempt(StudentAttempt(
            question_id="q1", student_answer="4", is_correct=True,
            timestamp=datetime.now(), time_taken_seconds=5,
            topic="math", difficulty=DifficultyLevel.EASY
        ))
        
        # Add science attempt
        perf.add_attempt(StudentAttempt(
            question_id="q2", student_answer="wrong", is_correct=False,
            timestamp=datetime.now(), time_taken_seconds=10,
            topic="science", difficulty=DifficultyLevel.EASY
        ))
        
        self.assertEqual(perf.get_topic_accuracy("math"), 100.0)
        self.assertEqual(perf.get_topic_accuracy("science"), 0.0)
    
    def test_difficulty_accuracy(self):
        """Test difficulty-specific accuracy."""
        perf = StudentPerformance(student_id="test_001")
        
        # Add easy correct
        perf.add_attempt(StudentAttempt(
            question_id="q1", student_answer="4", is_correct=True,
            timestamp=datetime.now(), time_taken_seconds=5,
            topic="math", difficulty=DifficultyLevel.EASY
        ))
        
        # Add medium incorrect
        perf.add_attempt(StudentAttempt(
            question_id="q2", student_answer="wrong", is_correct=False,
            timestamp=datetime.now(), time_taken_seconds=10,
            topic="math", difficulty=DifficultyLevel.MEDIUM
        ))
        
        self.assertEqual(perf.get_difficulty_accuracy(DifficultyLevel.EASY), 100.0)
        self.assertEqual(perf.get_difficulty_accuracy(DifficultyLevel.MEDIUM), 0.0)


class TestAnalyzer(unittest.TestCase):
    """Test StudentAnalyzer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = StudentAnalyzer()
        self.question = Question(
            id="q1",
            topic="algebra",
            difficulty=DifficultyLevel.EASY,
            content="What is 2 + 2?",
            correct_answer="4",
            explanation="2 + 2 = 4"
        )
    
    def test_analyze_correct_answer(self):
        """Test analyzing a correct answer."""
        attempt = self.analyzer.analyze_answer(
            student_id="student_001",
            question=self.question,
            student_answer="4",
            time_taken_seconds=5
        )
        
        self.assertTrue(attempt.is_correct)
        self.assertEqual(attempt.question_id, "q1")
        self.assertEqual(attempt.topic, "algebra")
    
    def test_analyze_incorrect_answer(self):
        """Test analyzing an incorrect answer."""
        attempt = self.analyzer.analyze_answer(
            student_id="student_001",
            question=self.question,
            student_answer="5",
            time_taken_seconds=10
        )
        
        self.assertFalse(attempt.is_correct)
    
    def test_case_insensitive_matching(self):
        """Test that answer checking is case-insensitive."""
        question = Question(
            id="q2",
            topic="science",
            difficulty=DifficultyLevel.EASY,
            content="What is H2O?",
            correct_answer="Water",
            explanation="H2O is water"
        )
        
        attempt = self.analyzer.analyze_answer(
            student_id="student_001",
            question=question,
            student_answer="water",
            time_taken_seconds=5
        )
        
        self.assertTrue(attempt.is_correct)
    
    def test_performance_tracking(self):
        """Test that performance is tracked correctly."""
        self.analyzer.analyze_answer(
            student_id="student_001",
            question=self.question,
            student_answer="4",
            time_taken_seconds=5
        )
        
        performance = self.analyzer.get_or_create_student("student_001")
        self.assertEqual(performance.total_attempts, 1)
        self.assertEqual(performance.correct_attempts, 1)
    
    def test_performance_summary(self):
        """Test performance summary generation."""
        self.analyzer.analyze_answer(
            student_id="student_001",
            question=self.question,
            student_answer="4",
            time_taken_seconds=5
        )
        
        summary = self.analyzer.get_performance_summary("student_001")
        
        self.assertEqual(summary["student_id"], "student_001")
        self.assertEqual(summary["total_attempts"], 1)
        self.assertEqual(summary["correct_attempts"], 1)
        self.assertEqual(summary["overall_accuracy"], 100.0)


class TestRuleEngine(unittest.TestCase):
    """Test RuleEngine."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.engine = RuleEngine()
    
    def test_first_question_rule(self):
        """Test rule for first-time student."""
        performance = StudentPerformance(student_id="test_001")
        decision = self.engine.decide_next_action(performance, "algebra")
        
        self.assertEqual(decision.next_action, NextAction.QUESTION)
        self.assertEqual(decision.difficulty, DifficultyLevel.EASY)
        self.assertIn("First question", decision.reason)
    
    def test_consecutive_incorrect_rule(self):
        """Test rule for consecutive incorrect answers."""
        performance = StudentPerformance(student_id="test_001")
        
        # Add 3 consecutive incorrect attempts
        for i in range(3):
            performance.add_attempt(StudentAttempt(
                question_id=f"q{i}",
                student_answer="wrong",
                is_correct=False,
                timestamp=datetime.now(),
                time_taken_seconds=10,
                topic="algebra",
                difficulty=DifficultyLevel.EASY
            ))
        
        decision = self.engine.decide_next_action(performance, "algebra")
        
        self.assertEqual(decision.next_action, NextAction.LESSON)
        self.assertIn("consecutive", decision.reason.lower())
    
    def test_low_topic_accuracy_rule(self):
        """Test rule for low topic accuracy."""
        performance = StudentPerformance(student_id="test_001")
        
        # Add attempts with low accuracy but not consecutive incorrect
        # Pattern: wrong, correct, wrong, correct, wrong (40% accuracy)
        for i in range(5):
            is_correct = (i % 2 == 1)  # Correct on odd indices
            performance.add_attempt(StudentAttempt(
                question_id=f"q{i}",
                student_answer="correct" if is_correct else "wrong",
                is_correct=is_correct,
                timestamp=datetime.now(),
                time_taken_seconds=10,
                topic="algebra",
                difficulty=DifficultyLevel.EASY
            ))
        
        decision = self.engine.decide_next_action(performance, "algebra")
        
        # Should trigger feedback due to low accuracy (40%)
        self.assertEqual(decision.next_action, NextAction.FEEDBACK)
    
    def test_difficulty_progression_rule(self):
        """Test rule for difficulty progression."""
        performance = StudentPerformance(student_id="test_001")
        
        # Add 5 correct easy attempts
        for i in range(5):
            performance.add_attempt(StudentAttempt(
                question_id=f"q{i}",
                student_answer="correct",
                is_correct=True,
                timestamp=datetime.now(),
                time_taken_seconds=5,
                topic="algebra",
                difficulty=DifficultyLevel.EASY
            ))
        
        decision = self.engine.decide_next_action(performance, "algebra")
        
        # Should progress to medium difficulty
        self.assertEqual(decision.next_action, NextAction.QUESTION)
        self.assertEqual(decision.difficulty, DifficultyLevel.MEDIUM)


class TestSystem(unittest.TestCase):
    """Test StudentPerformanceSystem integration."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.system = StudentPerformanceSystem()
        self.questions = create_sample_questions()
    
    def test_process_answer(self):
        """Test processing a student answer."""
        result = self.system.process_answer(
            student_id="student_001",
            question=self.questions[0],
            student_answer="4",
            time_taken_seconds=5,
            current_topic="algebra"
        )
        
        self.assertIn("attempt", result)
        self.assertIn("performance", result)
        self.assertIn("next_action", result)
        self.assertTrue(result["attempt"]["is_correct"])
    
    def test_get_next_action(self):
        """Test getting next action for student."""
        next_action = self.system.get_next_action_for_student(
            student_id="student_001",
            current_topic="algebra"
        )
        
        self.assertIn("action", next_action)
        self.assertIn("reason", next_action)
        self.assertIn("difficulty", next_action)
        self.assertEqual(next_action["action"], "question")
    
    def test_student_summary(self):
        """Test getting student summary."""
        # Process a few answers
        self.system.process_answer(
            student_id="student_001",
            question=self.questions[0],
            student_answer="4",
            time_taken_seconds=5,
            current_topic="algebra"
        )
        
        summary = self.system.get_student_summary("student_001")
        
        self.assertIn("student_id", summary)
        self.assertIn("total_attempts", summary)
        self.assertIn("overall_accuracy", summary)
        self.assertEqual(summary["total_attempts"], 1)
    
    def test_multiple_students(self):
        """Test tracking multiple students independently."""
        # Student 1
        self.system.process_answer(
            student_id="student_001",
            question=self.questions[0],
            student_answer="4",
            time_taken_seconds=5,
            current_topic="algebra"
        )
        
        # Student 2
        self.system.process_answer(
            student_id="student_002",
            question=self.questions[0],
            student_answer="5",
            time_taken_seconds=10,
            current_topic="algebra"
        )
        
        summary1 = self.system.get_student_summary("student_001")
        summary2 = self.system.get_student_summary("student_002")
        
        self.assertEqual(summary1["overall_accuracy"], 100.0)
        self.assertEqual(summary2["overall_accuracy"], 0.0)


if __name__ == "__main__":
    unittest.main()
