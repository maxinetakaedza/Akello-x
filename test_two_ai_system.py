"""
Unit tests for the extended two-AI system.
"""
import unittest
from datetime import datetime
from models import StudentPerformance, StudentAttempt, DifficultyLevel, Question
from extended_models import (
    UserTier, TrendDirection, GradeLevel,
    StudentInterests, StudyBuddyReport, CareerMappingReport
)
from studybuddy_ai import StudyBuddyAI
from career_mapping_ai import CareerMappingAI
from akello_ai_system import AkelloAISystem, create_demo_interests


class TestStudyBuddyAI(unittest.TestCase):
    """Test StudyBuddy AI module."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.studybuddy = StudyBuddyAI()
        self.performance = StudentPerformance(student_id="test_student")
        
        # Add some test attempts
        for i in range(10):
            attempt = StudentAttempt(
                question_id=f"q{i}",
                student_answer="answer",
                is_correct=(i % 2 == 0),
                timestamp=datetime.now(),
                time_taken_seconds=10,
                topic="algebra" if i < 5 else "geometry",
                difficulty=DifficultyLevel.EASY
            )
            self.performance.add_attempt(attempt)
    
    def test_analyze_performance_free_tier(self):
        """Test free tier analysis."""
        report = self.studybuddy.analyze_performance(
            student_id="test_student",
            performance=self.performance,
            tier=UserTier.FREE
        )
        
        self.assertIsInstance(report, StudyBuddyReport)
        self.assertEqual(report.tier, UserTier.FREE)
        self.assertEqual(report.student_id, "test_student")
        self.assertGreater(len(report.subject_strengths), 0)
    
    def test_analyze_performance_premium_tier(self):
        """Test premium tier analysis."""
        report = self.studybuddy.analyze_performance(
            student_id="test_student",
            performance=self.performance,
            tier=UserTier.PREMIUM
        )
        
        self.assertIsInstance(report, StudyBuddyReport)
        self.assertEqual(report.tier, UserTier.PREMIUM)
        # Premium should have more detailed explanations
        if report.mistake_explanations:
            self.assertIsNotNone(report.mistake_explanations[0].deep_explanation)
    
    def test_subject_strength_analysis(self):
        """Test subject strength calculation."""
        report = self.studybuddy.analyze_performance(
            student_id="test_student",
            performance=self.performance,
            tier=UserTier.FREE
        )
        
        # Should have analyzed both subjects
        subjects = [s.subject for s in report.subject_strengths]
        self.assertIn("algebra", subjects)
        self.assertIn("geometry", subjects)
        
        # Check strength scores are valid
        for subject_strength in report.subject_strengths:
            self.assertGreaterEqual(subject_strength.strength_score, 0)
            self.assertLessEqual(subject_strength.strength_score, 100)
    
    def test_weekly_mission_generation(self):
        """Test weekly mission creation."""
        report = self.studybuddy.analyze_performance(
            student_id="test_student",
            performance=self.performance,
            tier=UserTier.FREE
        )
        
        self.assertIsNotNone(report.weekly_mission)
        self.assertIsInstance(report.weekly_mission.title, str)
        self.assertGreater(report.weekly_mission.estimated_time_minutes, 0)
    
    def test_trend_calculation(self):
        """Test trend analysis."""
        report = self.studybuddy.analyze_performance(
            student_id="test_student",
            performance=self.performance,
            tier=UserTier.FREE
        )
        
        self.assertIn(
            report.overall_trend,
            [TrendDirection.IMPROVING, TrendDirection.STABLE, TrendDirection.DECLINING]
        )


class TestCareerMappingAI(unittest.TestCase):
    """Test Career Mapping AI module."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.career_mapper = CareerMappingAI()
        self.studybuddy = StudyBuddyAI()
        
        # Create test performance
        performance = StudentPerformance(student_id="test_student")
        for i in range(10):
            attempt = StudentAttempt(
                question_id=f"q{i}",
                student_answer="answer",
                is_correct=(i % 2 == 0),
                timestamp=datetime.now(),
                time_taken_seconds=10,
                topic="mathematics",
                difficulty=DifficultyLevel.MEDIUM
            )
            performance.add_attempt(attempt)
        
        # Get StudyBuddy report
        self.studybuddy_report = self.studybuddy.analyze_performance(
            student_id="test_student",
            performance=performance,
            tier=UserTier.FREE
        )
        
        # Create interests
        self.interests = create_demo_interests()
    
    def test_generate_career_recommendations(self):
        """Test career recommendation generation."""
        report = self.career_mapper.generate_career_recommendations(
            student_id="test_student",
            studybuddy_report=self.studybuddy_report,
            interests=self.interests,
            tier=UserTier.FREE
        )
        
        self.assertIsInstance(report, CareerMappingReport)
        self.assertEqual(report.tier, UserTier.FREE)
        self.assertEqual(len(report.career_paths), 5)
    
    def test_skill_ratings_calculation(self):
        """Test skill ratings are calculated."""
        report = self.career_mapper.generate_career_recommendations(
            student_id="test_student",
            studybuddy_report=self.studybuddy_report,
            interests=self.interests,
            tier=UserTier.FREE
        )
        
        self.assertGreater(len(report.skill_ratings), 0)
        
        # Check all skill ratings are in valid range
        for skill in report.skill_ratings:
            self.assertGreaterEqual(skill.rating, 0)
            self.assertLessEqual(skill.rating, 5)
    
    def test_career_match_scores(self):
        """Test career match scores are valid."""
        report = self.career_mapper.generate_career_recommendations(
            student_id="test_student",
            studybuddy_report=self.studybuddy_report,
            interests=self.interests,
            tier=UserTier.FREE
        )
        
        for career in report.career_paths:
            self.assertGreaterEqual(career.match_score, 0)
            self.assertLessEqual(career.match_score, 100)
            self.assertIsInstance(career.title, str)
            self.assertGreater(len(career.title), 0)
    
    def test_zimbabwe_examples_included(self):
        """Test Zimbabwe-specific examples are included."""
        report = self.career_mapper.generate_career_recommendations(
            student_id="test_student",
            studybuddy_report=self.studybuddy_report,
            interests=self.interests,
            tier=UserTier.FREE
        )
        
        # At least one career should have Zimbabwe examples
        has_examples = any(
            len(career.zimbabwe_examples) > 0 
            for career in report.career_paths
        )
        self.assertTrue(has_examples)
    
    def test_premium_features(self):
        """Test premium-only features."""
        free_report = self.career_mapper.generate_career_recommendations(
            student_id="test_student",
            studybuddy_report=self.studybuddy_report,
            interests=self.interests,
            tier=UserTier.FREE
        )
        
        premium_report = self.career_mapper.generate_career_recommendations(
            student_id="test_student",
            studybuddy_report=self.studybuddy_report,
            interests=self.interests,
            tier=UserTier.PREMIUM
        )
        
        # Free should not have premium features
        self.assertIsNone(free_report.skill_gap_analysis)
        self.assertIsNone(free_report.self_improvement_plan)
        
        # Premium should have premium features
        self.assertIsNotNone(premium_report.skill_gap_analysis)
        self.assertIsNotNone(premium_report.self_improvement_plan)
        self.assertGreater(len(premium_report.career_clusters), 0)


class TestAkelloAISystem(unittest.TestCase):
    """Test integrated AI system."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.ai_system = AkelloAISystem()
        
        # Create test performance
        self.performance = StudentPerformance(student_id="test_student")
        for i in range(10):
            attempt = StudentAttempt(
                question_id=f"q{i}",
                student_answer="answer",
                is_correct=True,
                timestamp=datetime.now(),
                time_taken_seconds=10,
                topic="algebra",
                difficulty=DifficultyLevel.EASY
            )
            self.performance.add_attempt(attempt)
        
        self.interests = create_demo_interests()
    
    def test_get_studybuddy_analysis(self):
        """Test getting StudyBuddy analysis."""
        report = self.ai_system.get_studybuddy_analysis(
            student_id="test_student",
            performance=self.performance,
            tier=UserTier.FREE
        )
        
        self.assertIsInstance(report, StudyBuddyReport)
    
    def test_get_career_recommendations(self):
        """Test getting career recommendations."""
        studybuddy_report = self.ai_system.get_studybuddy_analysis(
            student_id="test_student",
            performance=self.performance,
            tier=UserTier.FREE
        )
        
        career_report = self.ai_system.get_career_recommendations(
            student_id="test_student",
            studybuddy_report=studybuddy_report,
            interests=self.interests,
            tier=UserTier.FREE
        )
        
        self.assertIsInstance(career_report, CareerMappingReport)
    
    def test_get_complete_analysis(self):
        """Test getting complete analysis from both AIs."""
        result = self.ai_system.get_complete_analysis(
            student_id="test_student",
            performance=self.performance,
            interests=self.interests,
            tier=UserTier.FREE
        )
        
        self.assertIn("studybuddy_report", result)
        self.assertIn("career_report", result)
        self.assertIn("tier", result)
        self.assertEqual(result["tier"], "free")
    
    def test_format_studybuddy_report(self):
        """Test StudyBuddy report formatting."""
        report = self.ai_system.get_studybuddy_analysis(
            student_id="test_student",
            performance=self.performance,
            tier=UserTier.FREE
        )
        
        formatted = self.ai_system.format_studybuddy_report(report)
        
        self.assertIn("student_id", formatted)
        self.assertIn("overall_confidence", formatted)
        self.assertIn("subjects", formatted)
    
    def test_format_career_report(self):
        """Test Career report formatting."""
        studybuddy_report = self.ai_system.get_studybuddy_analysis(
            student_id="test_student",
            performance=self.performance,
            tier=UserTier.FREE
        )
        
        career_report = self.ai_system.get_career_recommendations(
            student_id="test_student",
            studybuddy_report=studybuddy_report,
            interests=self.interests,
            tier=UserTier.FREE
        )
        
        formatted = self.ai_system.format_career_report(career_report)
        
        self.assertIn("student_id", formatted)
        self.assertIn("skill_ratings", formatted)
        self.assertIn("top_careers", formatted)


class TestExtendedModels(unittest.TestCase):
    """Test extended data models."""
    
    def test_student_interests_creation(self):
        """Test StudentInterests model."""
        interests = StudentInterests(
            interests=["math", "science"],
            grade_level=GradeLevel.SECONDARY,
            age=15
        )
        
        self.assertEqual(len(interests.interests), 2)
        self.assertEqual(interests.grade_level, GradeLevel.SECONDARY)
    
    def test_user_tier_enum(self):
        """Test UserTier enum."""
        self.assertEqual(UserTier.FREE.value, "free")
        self.assertEqual(UserTier.PREMIUM.value, "premium")
    
    def test_trend_direction_enum(self):
        """Test TrendDirection enum."""
        self.assertIn(
            TrendDirection.IMPROVING,
            [TrendDirection.IMPROVING, TrendDirection.STABLE, TrendDirection.DECLINING]
        )


if __name__ == "__main__":
    unittest.main()
