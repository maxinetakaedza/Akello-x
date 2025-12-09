# Rule-Based Student Performance Analysis System

## Overview

This is a **rule-based supervised system** that analyzes student answers and performance to intelligently decide what to show next: questions, lessons, or feedback. The system uses explicit "if-then" rules and labeled data (student attempts, correctness, difficulty, topic tags) to make educational decisions.

## System Architecture

The system consists of four main components:

### 1. **Data Models** (`models.py`)
Defines the core data structures:
- `Question`: Represents questions with topic, difficulty, and correct answers
- `StudentAttempt`: Records each answer attempt with labeled data
- `StudentPerformance`: Tracks cumulative performance metrics
- `DecisionResult`: Contains the system's decision on what to show next
- `DifficultyLevel`: Enum for EASY, MEDIUM, HARD
- `NextAction`: Enum for QUESTION, LESSON, FEEDBACK

### 2. **Student Analyzer** (`analyzer.py`)
Processes and analyzes student answers:
- Validates answer correctness
- Tracks performance metrics by topic and difficulty
- Generates performance summaries and insights
- Maintains labeled training data (attempts, correctness, difficulty, topics)

### 3. **Rule Engine** (`rule_engine.py`)
Implements the core decision-making logic using explicit if-then rules:
- **Rule 1**: First-time students start with easy questions
- **Rule 2**: Consecutive failures trigger lesson review
- **Rule 3**: Low topic accuracy triggers feedback
- **Rule 4**: Recent performance decline triggers intervention
- **Rule 5**: Mastery of easy questions advances to medium
- **Rule 6**: Mastery of medium questions advances to hard
- **Rule 7**: Struggle with hard questions steps back to medium
- **Rule 8**: Good performance continues at same level
- **Default Rule**: Adaptive difficulty based on accuracy

### 4. **Main System** (`system.py`)
Integrates analyzer and rule engine:
- Processes student answers
- Applies rule-based decisions
- Provides student performance summaries
- Manages the complete learning workflow

## How It Works

The system follows a **supervised learning** approach with explicit rules:

1. **Data Collection**: Each student answer is labeled with:
   - Question ID
   - Correctness (binary label)
   - Difficulty level
   - Topic tag
   - Time taken
   - Timestamp

2. **Analysis**: The analyzer processes this labeled data to compute:
   - Overall accuracy
   - Topic-specific accuracy
   - Difficulty-specific accuracy
   - Recent performance trends

3. **Rule-Based Decision**: The rule engine applies if-then rules:
   ```
   IF student has no attempts THEN show easy question
   IF consecutive_incorrect >= 3 THEN show lesson
   IF topic_accuracy < 50% THEN show feedback
   IF easy_accuracy >= 90% THEN increase to medium difficulty
   ... (more rules)
   ```

4. **Action**: The system decides to show:
   - **QUESTION**: Next practice question at appropriate difficulty
   - **LESSON**: Review material for struggling topics
   - **FEEDBACK**: Detailed performance feedback and guidance

## Installation

No external dependencies required - uses Python standard library only.

```bash
# Clone the repository
git clone https://github.com/maxinetakaedza/Akello-x.git
cd Akello-x

# Run the demo
python system.py
```

## Usage Examples

### Basic Usage

```python
from system import StudentPerformanceSystem, create_sample_questions
from models import Question, DifficultyLevel

# Initialize the system
system = StudentPerformanceSystem()

# Create or get sample questions
questions = create_sample_questions()

# Process a student answer
result = system.process_answer(
    student_id="student_123",
    question=questions[0],
    student_answer="4",
    time_taken_seconds=5,
    current_topic="algebra"
)

# Check the result
print(f"Answer correct: {result['attempt']['is_correct']}")
print(f"Next action: {result['next_action']['action']}")
print(f"Message: {result['next_action']['message']}")
```

### Get Next Action Without Answer

```python
# Get recommendation for what to show next
next_action = system.get_next_action_for_student(
    student_id="student_123",
    current_topic="algebra"
)

print(f"Show: {next_action['action']}")
print(f"Difficulty: {next_action['difficulty']}")
print(f"Reason: {next_action['reason']}")
```

### Get Performance Summary

```python
# Get comprehensive performance data
summary = system.get_student_summary("student_123")

print(f"Total attempts: {summary['total_attempts']}")
print(f"Accuracy: {summary['overall_accuracy']:.1f}%")
print(f"Topic breakdown: {summary['topic_accuracy']}")
print(f"Recent attempts: {summary['recent_attempts']}")
```

### Creating Custom Questions

```python
from models import Question, DifficultyLevel

question = Question(
    id="custom_1",
    topic="calculus",
    difficulty=DifficultyLevel.MEDIUM,
    content="What is the derivative of x^2?",
    correct_answer="2x",
    explanation="Using the power rule: d/dx(x^n) = n*x^(n-1)"
)
```

## Rule Configuration

You can customize the rule thresholds in `RuleEngine`:

```python
from rule_engine import RuleEngine

engine = RuleEngine()
# Customize thresholds
engine.LOW_ACCURACY_THRESHOLD = 60.0  # Default: 50.0
engine.MEDIUM_ACCURACY_THRESHOLD = 80.0  # Default: 75.0
engine.HIGH_ACCURACY_THRESHOLD = 95.0  # Default: 90.0
engine.CONSECUTIVE_INCORRECT_THRESHOLD = 2  # Default: 3
```

## Decision Logic Flow

```
Student Answer
    ↓
Analyze (correct/incorrect, time, topic, difficulty)
    ↓
Update Performance Metrics
    ↓
Apply Rule-Based Decision Engine
    ↓
Decision: QUESTION / LESSON / FEEDBACK
    ↓
Return with appropriate difficulty and message
```

## Key Features

✅ **Rule-Based Supervised System**: Uses explicit if-then rules
✅ **Labeled Data**: Tracks attempts with correctness, difficulty, topics
✅ **Adaptive Difficulty**: Automatically adjusts question difficulty
✅ **Topic Tracking**: Monitors performance across different topics
✅ **Performance Analytics**: Comprehensive metrics and insights
✅ **Intervention Logic**: Triggers lessons/feedback when needed
✅ **No External Dependencies**: Pure Python implementation

## Example Output

```
==============================================================
Rule-Based Student Performance Analysis System
==============================================================

Student: student_001, Topic: algebra

Question 1: What is 2 + 2?
Correct: True
Next Action: question
Message: Welcome! Let's start with a warm-up question.

Question 2: What is 5 * 3?
Correct: True
Next Action: question
Message: Great job! Let's try a medium difficulty question.

==============================================================
Student Performance Summary
==============================================================
Total Attempts: 2
Correct Attempts: 2
Overall Accuracy: 100.0%
Topic Accuracy: {'algebra': 100.0}
```

## Contributing

This is part of the Akello-x project for educational AI improvements. Contributions welcome!

## License

See repository license.
