# Quick Start Guide

## Rule-Based Student Performance Analysis System

### Installation

No installation required! The system uses only Python standard library.

```bash
git clone https://github.com/maxinetakaedza/Akello-x.git
cd Akello-x
```

### Running the System

#### 1. Basic Demo
```bash
python system.py
```
See a simple demonstration of the system processing student answers.

#### 2. Interactive Demo
```bash
python interactive_demo.py
```
Watch a complete learning journey simulation with visual analytics.

#### 3. Comprehensive Examples
```bash
python example_usage.py
```
See 6 detailed scenarios demonstrating all system features.

#### 4. Run Tests
```bash
python -m unittest test_system.py -v
```
Verify all 18 unit tests pass.

### Basic Usage

```python
from system import StudentPerformanceSystem
from models import Question, DifficultyLevel

# Initialize
system = StudentPerformanceSystem()

# Create a question
question = Question(
    id="q1",
    topic="algebra",
    difficulty=DifficultyLevel.EASY,
    content="What is 2 + 2?",
    correct_answer="4",
    explanation="Basic addition"
)

# Process student answer
result = system.process_answer(
    student_id="student_123",
    question=question,
    student_answer="4",
    time_taken_seconds=5,
    current_topic="algebra"
)

# Check result
print(f"Correct: {result['attempt']['is_correct']}")
print(f"Next: {result['next_action']['action']}")
print(f"Message: {result['next_action']['message']}")
```

### Understanding the Output

The system returns three things:
1. **Attempt Analysis**: Was the answer correct?
2. **Performance Metrics**: Current accuracy and statistics
3. **Next Action**: What to show next (question/lesson/feedback)

### Key Concepts

**Actions:**
- `QUESTION`: Show next practice question
- `LESSON`: Show review material  
- `FEEDBACK`: Show performance feedback

**Difficulty Levels:**
- `EASY`: Beginner level
- `MEDIUM`: Intermediate level
- `HARD`: Advanced level

**Rule-Based Logic:**
The system uses 9 if-then rules to decide what's best for each student based on their performance.

### File Structure

```
Akello-x/
├── models.py           # Data models
├── analyzer.py         # Answer analyzer
├── rule_engine.py      # Decision rules
├── system.py           # Main system
├── test_system.py      # Unit tests
├── example_usage.py    # Examples
├── interactive_demo.py # Interactive demo
├── README.md           # Overview
└── README_SYSTEM.md    # Full documentation
```

### Next Steps

1. Read [README_SYSTEM.md](README_SYSTEM.md) for detailed documentation
2. Run the examples to see different scenarios
3. Customize the rules in `rule_engine.py` if needed
4. Add your own questions using the `Question` model

### Getting Help

See the full documentation in README_SYSTEM.md for:
- Complete API reference
- Advanced configuration
- Custom question creation
- Performance tracking details
