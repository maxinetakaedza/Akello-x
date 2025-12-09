"""
Extended data models for the two-AI architecture.
Includes StudyBuddy AI and Career Mapping AI data structures.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum


class UserTier(Enum):
    """User subscription tier."""
    FREE = "free"
    PREMIUM = "premium"


class TrendDirection(Enum):
    """Performance trend direction."""
    IMPROVING = "improving"
    STABLE = "stable"
    DECLINING = "declining"


class GradeLevel(Enum):
    """Student grade level."""
    PRIMARY = "primary"
    SECONDARY = "secondary"


@dataclass
class SubjectStrength:
    """Represents strength/weakness analysis for a subject."""
    subject: str
    strength_score: float  # 0-100
    weakness_score: float  # 0-100
    confidence_score: float  # 0-100
    trend: TrendDirection
    pain_points: List[str] = field(default_factory=list)
    mastery_level: str = "beginner"  # beginner, intermediate, advanced


@dataclass
class WeeklyMission:
    """Represents a weekly learning mission."""
    mission_id: str
    subject: str
    title: str
    description: str
    target_topics: List[str]
    difficulty_focus: str  # "easy", "medium", "hard"
    estimated_time_minutes: int


@dataclass
class MistakeExplanation:
    """Explanation for a student's mistake."""
    question_id: str
    student_answer: str
    correct_answer: str
    basic_explanation: str
    deep_explanation: Optional[str] = None  # Premium only
    related_concepts: List[str] = field(default_factory=list)
    remediation_steps: List[str] = field(default_factory=list)


@dataclass
class StudyBuddyReport:
    """Output from StudyBuddy AI (weekly or real-time)."""
    student_id: str
    report_date: datetime
    tier: UserTier
    
    # Subject analysis
    subject_strengths: List[SubjectStrength] = field(default_factory=list)
    
    # Overall metrics
    overall_confidence: float = 0.0
    overall_trend: TrendDirection = TrendDirection.STABLE
    
    # Topic difficulty mapping
    topic_difficulty_map: Dict[str, float] = field(default_factory=dict)
    
    # Recommendations
    recommended_quizzes: List[str] = field(default_factory=list)
    weekly_mission: Optional[WeeklyMission] = None
    
    # Explanations (limited for free tier)
    mistake_explanations: List[MistakeExplanation] = field(default_factory=list)
    
    # Pain points for Career AI
    pain_points: List[str] = field(default_factory=list)


@dataclass
class StudentInterests:
    """Student interests and preferences for career mapping."""
    interests: List[str] = field(default_factory=list)
    disinterests: List[str] = field(default_factory=list)
    favorite_subjects: List[str] = field(default_factory=list)
    least_favorite_subjects: List[str] = field(default_factory=list)
    free_text_reflections: List[str] = field(default_factory=list)
    grade_level: GradeLevel = GradeLevel.SECONDARY
    age: int = 15


@dataclass
class SkillRating:
    """Skill rating for career matching."""
    skill_name: str
    rating: float  # 0-5 stars
    evidence: str  # Why this rating


@dataclass
class CareerPath:
    """Represents a recommended career path."""
    career_id: str
    title: str
    match_score: float  # 0-100
    
    # Skill ratings
    problem_solving: float = 0.0  # 0-5
    creativity: float = 0.0
    people_skills: float = 0.0
    tech_affinity: float = 0.0
    analytical_skills: float = 0.0
    
    # Details
    why_matched: str = ""
    skills_needed: List[str] = field(default_factory=list)
    zimbabwe_examples: List[str] = field(default_factory=list)
    
    # Resources
    recommended_articles: List[str] = field(default_factory=list)
    recommended_videos: List[str] = field(default_factory=list)
    reading_list: List[str] = field(default_factory=list)


@dataclass
class CareerMappingReport:
    """Output from Career Mapping AI."""
    student_id: str
    report_date: datetime
    tier: UserTier
    
    # Recommended careers
    career_paths: List[CareerPath] = field(default_factory=list)
    
    # Skill analysis
    skill_ratings: List[SkillRating] = field(default_factory=list)
    
    # Premium features
    skill_gap_analysis: Optional[str] = None  # Premium only
    self_improvement_plan: Optional[str] = None  # Premium only
    career_clusters: List[str] = field(default_factory=list)  # Premium only
