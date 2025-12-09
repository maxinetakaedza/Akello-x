"""
Integrated Two-AI System
Combines StudyBuddy AI and Career Mapping AI for complete student support.
"""
from typing import Optional
from datetime import datetime
from models import StudentPerformance
from extended_models import (
    UserTier, StudentInterests, GradeLevel,
    StudyBuddyReport, CareerMappingReport
)
from studybuddy_ai import StudyBuddyAI
from career_mapping_ai import CareerMappingAI


class AkelloAISystem:
    """
    Complete Akello AI System with both StudyBuddy and Career Mapping.
    
    This is the main interface for the prototype two-AI architecture.
    """
    
    def __init__(self):
        """Initialize both AI systems."""
        self.studybuddy = StudyBuddyAI()
        self.career_mapper = CareerMappingAI()
    
    def get_studybuddy_analysis(
        self,
        student_id: str,
        performance: StudentPerformance,
        tier: UserTier = UserTier.FREE
    ) -> StudyBuddyReport:
        """
        Get StudyBuddy AI analysis.
        
        FREE tier: Weekly batch analysis only
        PREMIUM tier: Real-time analysis anytime
        
        Args:
            student_id: Student identifier
            performance: Student's performance data
            tier: User subscription tier
            
        Returns:
            StudyBuddyReport with analysis and recommendations
        """
        return self.studybuddy.analyze_performance(
            student_id=student_id,
            performance=performance,
            tier=tier
        )
    
    def get_career_recommendations(
        self,
        student_id: str,
        studybuddy_report: StudyBuddyReport,
        interests: StudentInterests,
        tier: UserTier = UserTier.FREE
    ) -> CareerMappingReport:
        """
        Get Career Mapping AI recommendations.
        
        Runs weekly after StudyBuddy analysis.
        
        Args:
            student_id: Student identifier
            studybuddy_report: Output from StudyBuddy AI
            interests: Student's interests and preferences
            tier: User subscription tier
            
        Returns:
            CareerMappingReport with career recommendations
        """
        return self.career_mapper.generate_career_recommendations(
            student_id=student_id,
            studybuddy_report=studybuddy_report,
            interests=interests,
            tier=tier
        )
    
    def get_complete_analysis(
        self,
        student_id: str,
        performance: StudentPerformance,
        interests: StudentInterests,
        tier: UserTier = UserTier.FREE
    ) -> dict:
        """
        Get complete analysis from both AI systems.
        
        This is a convenience method that runs both AIs in sequence.
        
        Args:
            student_id: Student identifier
            performance: Student's performance data
            interests: Student's interests and preferences
            tier: User subscription tier
            
        Returns:
            Dictionary containing both reports
        """
        # Step 1: StudyBuddy Analysis
        studybuddy_report = self.get_studybuddy_analysis(
            student_id=student_id,
            performance=performance,
            tier=tier
        )
        
        # Step 2: Career Mapping (runs after StudyBuddy)
        career_report = self.get_career_recommendations(
            student_id=student_id,
            studybuddy_report=studybuddy_report,
            interests=interests,
            tier=tier
        )
        
        return {
            "studybuddy_report": studybuddy_report,
            "career_report": career_report,
            "tier": tier.value,
            "generated_at": datetime.now().isoformat()
        }
    
    def format_studybuddy_report(
        self, report: StudyBuddyReport
    ) -> dict:
        """Format StudyBuddy report for easy consumption."""
        return {
            "student_id": report.student_id,
            "tier": report.tier.value,
            "report_date": report.report_date.isoformat(),
            "overall_confidence": round(report.overall_confidence, 1),
            "overall_trend": report.overall_trend.value,
            "subjects": [
                {
                    "name": s.subject,
                    "strength": round(s.strength_score, 1),
                    "weakness": round(s.weakness_score, 1),
                    "confidence": round(s.confidence_score, 1),
                    "trend": s.trend.value,
                    "mastery": s.mastery_level,
                    "pain_points": s.pain_points
                }
                for s in report.subject_strengths
            ],
            "topic_difficulty": report.topic_difficulty_map,
            "recommended_quizzes": report.recommended_quizzes,
            "weekly_mission": {
                "title": report.weekly_mission.title,
                "subject": report.weekly_mission.subject,
                "description": report.weekly_mission.description,
                "estimated_time": report.weekly_mission.estimated_time_minutes
            } if report.weekly_mission else None,
            "mistake_count": len(report.mistake_explanations),
            "has_deep_explanations": report.tier == UserTier.PREMIUM
        }
    
    def format_career_report(
        self, report: CareerMappingReport
    ) -> dict:
        """Format Career Mapping report for easy consumption."""
        return {
            "student_id": report.student_id,
            "tier": report.tier.value,
            "report_date": report.report_date.isoformat(),
            "skill_ratings": [
                {
                    "skill": sr.skill_name,
                    "rating": round(sr.rating, 1),
                    "evidence": sr.evidence
                }
                for sr in report.skill_ratings
            ],
            "top_careers": [
                {
                    "title": cp.title,
                    "match_score": round(cp.match_score, 1),
                    "skills": {
                        "problem_solving": round(cp.problem_solving, 1),
                        "creativity": round(cp.creativity, 1),
                        "people_skills": round(cp.people_skills, 1),
                        "tech_affinity": round(cp.tech_affinity, 1),
                        "analytical_skills": round(cp.analytical_skills, 1)
                    },
                    "why_matched": cp.why_matched,
                    "zimbabwe_examples": cp.zimbabwe_examples
                }
                for cp in report.career_paths
            ],
            "has_premium_analysis": report.tier == UserTier.PREMIUM,
            "skill_gap_analysis": report.skill_gap_analysis if report.tier == UserTier.PREMIUM else None,
            "career_clusters": report.career_clusters if report.tier == UserTier.PREMIUM else []
        }


def create_demo_interests() -> StudentInterests:
    """Create demo student interests for testing."""
    return StudentInterests(
        interests=["technology", "problem solving", "helping others", "mathematics"],
        disinterests=["public speaking", "sales"],
        favorite_subjects=["mathematics", "computer science"],
        least_favorite_subjects=["literature"],
        free_text_reflections=["I enjoy logical puzzles", "Math makes sense to me"],
        grade_level=GradeLevel.SECONDARY,
        age=16
    )


if __name__ == "__main__":
    """Demonstration of the complete two-AI system."""
    from system import StudentPerformanceSystem, create_sample_questions
    
    print("="*80)
    print("AKELLO TWO-AI SYSTEM DEMONSTRATION")
    print("="*80)
    
    # Initialize systems
    ai_system = AkelloAISystem()
    performance_system = StudentPerformanceSystem()
    questions = create_sample_questions()
    
    # Simulate student activity
    student_id = "demo_student_001"
    
    print(f"\n📚 Simulating student activity for {student_id}...")
    
    # Student answers several questions
    for i, q in enumerate(questions[:6]):
        answer = q.correct_answer if i % 2 == 0 else "wrong"
        performance_system.process_answer(
            student_id=student_id,
            question=q,
            student_answer=answer,
            time_taken_seconds=10 + i*2,
            current_topic=q.topic
        )
    
    # Get student performance
    performance = performance_system.analyzer.get_or_create_student(student_id)
    
    # Create student interests
    interests = create_demo_interests()
    
    print("\n" + "="*80)
    print("FREE TIER ANALYSIS")
    print("="*80)
    
    # Get FREE tier analysis
    free_analysis = ai_system.get_complete_analysis(
        student_id=student_id,
        performance=performance,
        interests=interests,
        tier=UserTier.FREE
    )
    
    # Display StudyBuddy Report (Free)
    print("\n📊 STUDYBUDDY AI REPORT (Free Tier)")
    print("-"*80)
    studybuddy_formatted = ai_system.format_studybuddy_report(
        free_analysis["studybuddy_report"]
    )
    print(f"Overall Confidence: {studybuddy_formatted['overall_confidence']}%")
    print(f"Trend: {studybuddy_formatted['overall_trend']}")
    print(f"\nSubjects Analyzed:")
    for subject in studybuddy_formatted['subjects']:
        print(f"  • {subject['name']}: {subject['mastery']} "
              f"(Strength: {subject['strength']}%, Confidence: {subject['confidence']}%)")
    
    if studybuddy_formatted['weekly_mission']:
        print(f"\nWeekly Mission: {studybuddy_formatted['weekly_mission']['title']}")
        print(f"  {studybuddy_formatted['weekly_mission']['description']}")
    
    # Display Career Report (Free)
    print("\n\n🎯 CAREER MAPPING AI REPORT (Free Tier)")
    print("-"*80)
    career_formatted = ai_system.format_career_report(
        free_analysis["career_report"]
    )
    print("Skill Ratings:")
    for skill in career_formatted['skill_ratings']:
        stars = "★" * int(skill['rating']) + "☆" * (5 - int(skill['rating']))
        print(f"  {skill['skill']}: {stars} ({skill['rating']}/5)")
    
    print(f"\nTop 5 Career Matches:")
    for i, career in enumerate(career_formatted['top_careers'], 1):
        print(f"\n  {i}. {career['title']} ({career['match_score']}% match)")
        print(f"     {career['why_matched']}")
        if career['zimbabwe_examples']:
            print(f"     Zimbabwe example: {career['zimbabwe_examples'][0]}")
    
    # PREMIUM TIER
    print("\n\n" + "="*80)
    print("PREMIUM TIER ANALYSIS")
    print("="*80)
    
    premium_analysis = ai_system.get_complete_analysis(
        student_id=student_id,
        performance=performance,
        interests=interests,
        tier=UserTier.PREMIUM
    )
    
    premium_career = ai_system.format_career_report(
        premium_analysis["career_report"]
    )
    
    print("\n🌟 PREMIUM FEATURES:")
    if premium_career['skill_gap_analysis']:
        print("\nSkill Gap Analysis:")
        print(premium_career['skill_gap_analysis'])
    
    if premium_career['career_clusters']:
        print(f"\nCareer Clusters: {', '.join(premium_career['career_clusters'])}")
    
    print("\n" + "="*80)
    print("✅ TWO-AI SYSTEM DEMONSTRATION COMPLETE")
    print("="*80)
    print("\nKey Features Demonstrated:")
    print("  ✓ StudyBuddy AI with free/premium tiers")
    print("  ✓ Career Mapping AI with skill matching")
    print("  ✓ Weekly batch analysis (free) vs real-time (premium)")
    print("  ✓ Basic vs deep explanations")
    print("  ✓ Zimbabwe-specific career examples")
    print("  ✓ Complete two-AI pipeline integration")
