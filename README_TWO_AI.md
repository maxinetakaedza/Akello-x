# Akello-x Two-AI Architecture

## Overview

This repository implements a **complete two-AI system** for adaptive student learning and career guidance. The system includes:

1. **StudyBuddy AI** - Tracks performance over time and provides learning recommendations
2. **Career Mapping AI** - Recommends career paths based on strengths and interests

Both AIs support **Free** and **Premium** tiers with different feature sets.

---

## System Architecture

### AI #1: StudyBuddy AI

**Purpose**: Tracks student performance in Study Sessions and Quizzes

**Input Sources**:
- Subject chosen for session
- Topic/subtopic
- Quiz scores (correct vs wrong answers)
- Time taken per question
- Mistake patterns
- Frequency of studying each subject
- Engagement duration
- Difficulty ratings
- Weekly self-reflections

**Outputs**:
- Per-subject strength/weakness scores
- Confidence scores
- Performance trends (improving/stable/declining)
- Topic difficulty mapping
- Pain points analysis
- Weekly recommended quizzes
- Weekly "fix-your-weakness" mission
- Mistake explanations (basic for free, deep for premium)

**Free vs Premium**:

| Feature | Free Tier | Premium Tier |
|---------|-----------|--------------|
| Analysis Frequency | Weekly batch | Real-time anytime |
| Explanations | Basic | Deep, multi-step reasoning |
| Trend Analysis | Simple chart | Predictions & pathways |
| Missions | One per week | On-demand evaluations |
| Feedback | Basic | Teacher-style detailed |

---

### AI #2: Career Mapping AI

**Purpose**: Recommends career paths based on performance and interests

**Input Sources**:
- Interests and disinterests
- Strengths/weaknesses from StudyBuddy AI
- Engagement frequency
- Favorite/least favorite subjects
- Free-text reflections
- Grade level (primary/secondary)
- Age

**Outputs**:
- 5 recommended career paths
- Skill ratings (problem-solving, creativity, people skills, tech affinity, analytical)
- Why each career matches
- Zimbabwe-specific examples
- Recommended resources (articles, videos, books)
- Skills needed for each career

**Free vs Premium**:

| Feature | Free Tier | Premium Tier |
|---------|-----------|--------------|
| Career Matches | 5 careers with basic info | 5 careers with detailed analysis |
| Explanations | Simple matching | Deep reasoning with evidence |
| Skill Analysis | Basic ratings | Full skill gap analysis |
| Resources | Limited | Complete learning pathways |
| Career Insights | General | Zimbabwe-specific with clusters |

---

## Quick Start

### Installation

No external dependencies required - uses Python standard library only.

```bash
git clone https://github.com/maxinetakaedza/Akello-x.git
cd Akello-x
```

### Running the Complete System

```bash
# Run the integrated two-AI demonstration
python akello_ai_system.py

# Run the original rule-based system
python system.py

# Run comprehensive examples
python example_usage.py

# Run interactive demo
python interactive_demo.py
```

### Running Tests

```bash
# Test the two-AI system
python -m unittest test_two_ai_system.py -v

# Test the original rule engine
python -m unittest test_system.py -v
```

---

## Usage Examples

### Basic Two-AI Usage

```python
from akello_ai_system import AkelloAISystem, create_demo_interests
from models import StudentPerformance
from extended_models import UserTier

# Initialize the system
ai_system = AkelloAISystem()

# Get student performance data (from your database)
performance = get_student_performance("student_123")

# Get student interests
interests = create_demo_interests()

# Get complete analysis from both AIs
result = ai_system.get_complete_analysis(
    student_id="student_123",
    performance=performance,
    interests=interests,
    tier=UserTier.FREE  # or UserTier.PREMIUM
)

# Access StudyBuddy results
studybuddy = result['studybuddy_report']
print(f"Overall Confidence: {studybuddy.overall_confidence}%")
print(f"Trend: {studybuddy.overall_trend.value}")

# Access Career Mapping results
careers = result['career_report']
for career in careers.career_paths[:3]:
    print(f"{career.title}: {career.match_score}% match")
```

### StudyBuddy AI Only

```python
from studybuddy_ai import StudyBuddyAI
from extended_models import UserTier

studybuddy = StudyBuddyAI()

report = studybuddy.analyze_performance(
    student_id="student_123",
    performance=performance,
    tier=UserTier.PREMIUM  # Real-time analysis
)

# View subject strengths
for subject in report.subject_strengths:
    print(f"{subject.subject}:")
    print(f"  Strength: {subject.strength_score}%")
    print(f"  Mastery: {subject.mastery_level}")
    print(f"  Trend: {subject.trend.value}")
```

### Career Mapping AI Only

```python
from career_mapping_ai import CareerMappingAI
from extended_models import StudentInterests, GradeLevel

career_mapper = CareerMappingAI()

interests = StudentInterests(
    interests=["technology", "problem solving"],
    favorite_subjects=["mathematics", "physics"],
    grade_level=GradeLevel.SECONDARY,
    age=16
)

career_report = career_mapper.generate_career_recommendations(
    student_id="student_123",
    studybuddy_report=studybuddy_report,
    interests=interests,
    tier=UserTier.PREMIUM
)

# View top career matches
for career in career_report.career_paths:
    print(f"{career.title} ({career.match_score}% match)")
    print(f"  Why: {career.why_matched}")
    print(f"  Example: {career.zimbabwe_examples[0]}")
```

---

## File Structure

### Core System Files

```
Akello-x/
├── models.py                  # Original data models (Question, StudentAttempt, etc.)
├── extended_models.py         # Extended models for two-AI system
├── analyzer.py                # Student answer analyzer
├── rule_engine.py             # Original rule-based decision engine
├── studybuddy_ai.py          # AI #1: StudyBuddy AI
├── career_mapping_ai.py      # AI #2: Career Mapping AI
├── akello_ai_system.py       # Integrated two-AI system
├── system.py                  # Original integration system
```

### Testing & Examples

```
├── test_system.py             # Tests for original system
├── test_two_ai_system.py     # Tests for two-AI system
├── example_usage.py           # Usage examples
├── interactive_demo.py        # Interactive demonstration
```

### Documentation

```
├── README.md                  # This file
├── README_SYSTEM.md          # Original system documentation
├── QUICKSTART.md             # Quick start guide
├── IMPLEMENTATION_SUMMARY.txt # Implementation details
```

---

## Key Features

### ✅ Two-AI Architecture
- StudyBuddy AI for performance tracking
- Career Mapping AI for career guidance
- Weekly batch processing (free) or real-time (premium)

### ✅ Free vs Premium Tiers
- Configurable feature sets
- Basic vs deep analysis
- Limited vs unlimited access

### ✅ Zimbabwe-Specific Content
- Local career examples (Econet, Deloitte ZW, ZINWA, etc.)
- Context-appropriate recommendations
- Regional career clusters

### ✅ Comprehensive Analytics
- Subject strength/weakness scores
- Confidence and trend analysis
- Skill ratings (5 dimensions)
- Career matching algorithm

### ✅ Adaptive Learning
- Weekly missions based on weaknesses
- Personalized quiz recommendations
- Mistake explanations with remediation

### ✅ Production Ready
- 36+ unit tests (all passing)
- Zero external dependencies
- Clean architecture with separation of concerns
- Comprehensive error handling

---

## API Reference

### AkelloAISystem

Main integration class for both AIs.

```python
system = AkelloAISystem()

# Get StudyBuddy analysis
studybuddy_report = system.get_studybuddy_analysis(
    student_id: str,
    performance: StudentPerformance,
    tier: UserTier
)

# Get Career recommendations
career_report = system.get_career_recommendations(
    student_id: str,
    studybuddy_report: StudyBuddyReport,
    interests: StudentInterests,
    tier: UserTier
)

# Get complete analysis
complete = system.get_complete_analysis(
    student_id: str,
    performance: StudentPerformance,
    interests: StudentInterests,
    tier: UserTier
)
```

### StudyBuddyAI

Performance tracking and learning recommendations.

```python
studybuddy = StudyBuddyAI()

report = studybuddy.analyze_performance(
    student_id: str,
    performance: StudentPerformance,
    tier: UserTier
) -> StudyBuddyReport
```

### CareerMappingAI

Career path recommendations.

```python
career_mapper = CareerMappingAI()

report = career_mapper.generate_career_recommendations(
    student_id: str,
    studybuddy_report: StudyBuddyReport,
    interests: StudentInterests,
    tier: UserTier
) -> CareerMappingReport
```

---

## Data Models

### Key Enums

```python
UserTier.FREE          # Weekly batch analysis
UserTier.PREMIUM       # Real-time analysis

TrendDirection.IMPROVING
TrendDirection.STABLE
TrendDirection.DECLINING

GradeLevel.PRIMARY
GradeLevel.SECONDARY
```

### Main Data Structures

- `StudyBuddyReport` - Output from AI #1
- `CareerMappingReport` - Output from AI #2
- `SubjectStrength` - Subject analysis
- `CareerPath` - Career recommendation
- `SkillRating` - Skill assessment
- `StudentInterests` - Student preferences

---

## Testing

The system includes comprehensive tests:

```bash
# Run all tests
python -m unittest discover -v

# Run specific test suites
python -m unittest test_two_ai_system.py -v
python -m unittest test_system.py -v
```

**Test Coverage**:
- 18 tests for two-AI system
- 18 tests for original rule engine
- **36 total tests, all passing**

---

## Examples Output

### StudyBuddy Report (Free Tier)

```
Overall Confidence: 65.5%
Trend: improving

Subjects:
  • Mathematics: intermediate (Strength: 75%, Confidence: 70%)
  • Physics: beginner (Strength: 55%, Confidence: 60%)

Weekly Mission: Master Physics
  Focus on improving your Physics skills this week
```

### Career Report (Premium Tier)

```
Top Career Match: Software Engineer (82% match)
  Why: Your strong Analytical Skills and Tech Affinity align well

Skill Ratings:
  Problem Solving: ★★★★☆ (4.2/5)
  Tech Affinity: ★★★★★ (4.8/5)
  Analytical: ★★★★☆ (4.5/5)

Zimbabwe Example: Developers at Econet Wireless Zimbabwe

Skill Gap Analysis:
  Strengths: Already meet analytical and tech requirements
  To Develop: People Skills (+1.2 points)
```

---

## Contributing

This system is designed as a prototype. Future enhancements could include:

- Database integration
- API endpoints for web/mobile
- More career paths
- Machine learning for better predictions
- Real-time notification system
- Gamification elements

---

## License

See repository license.

---

## Contact

Part of the Akello-x project for educational improvement in Zimbabwe.
