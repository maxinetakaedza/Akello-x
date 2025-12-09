# Akello-x
IMPROVEMENT ON EXISTING AKELLO SERVICE AND HACKATHON CHALLENGE

## Complete Two-AI System for Adaptive Learning & Career Guidance

This repository implements a **complete prototype two-AI architecture** for student support:

1. **StudyBuddy AI** - Analyzes performance, provides learning recommendations
2. **Career Mapping AI** - Recommends career paths based on strengths and interests

Both systems support **Free** and **Premium** tiers with differentiated features.

📖 **[Complete Two-AI Documentation](README_TWO_AI.md)**

---

## Original Rule-Based System

Also includes the foundation **rule-based supervised system** that analyzes student answers and performance to intelligently decide what to show next: **questions**, **lessons**, or **feedback**.

### Key Features

✅ **Rule-Based Decision Engine**: Uses explicit if-then rules for educational decisions  
✅ **Supervised Learning Approach**: Tracks labeled data (attempts, correctness, difficulty, topics)  
✅ **Adaptive Difficulty**: Automatically adjusts question difficulty based on performance  
✅ **Multi-Topic Support**: Tracks performance across different subjects  
✅ **Smart Interventions**: Triggers lessons/feedback when students struggle  
✅ **Comprehensive Analytics**: Detailed performance metrics and insights  

### Quick Start

**Two-AI System:**
```bash
# Run the complete two-AI demonstration
python akello_ai_system.py

# Run tests for two-AI system
python -m unittest test_two_ai_system.py -v
```

**Original Rule-Based System:**
```bash
# Run the demo
python system.py

# Run comprehensive examples
python example_usage.py

# Run tests
python -m unittest test_system.py -v
```

### System Components

- **`models.py`**: Data models for questions, attempts, and performance
- **`analyzer.py`**: Analyzes student answers and tracks metrics
- **`rule_engine.py`**: Rule-based decision engine with if-then logic
- **`system.py`**: Main integration system
- **`test_system.py`**: Comprehensive unit tests
- **`example_usage.py`**: Detailed usage examples

### Documentation

For detailed documentation, see [README_SYSTEM.md](README_SYSTEM.md)

### How It Works

1. **Student answers a question** → labeled data recorded (correct/incorrect, topic, difficulty, time)
2. **System analyzes performance** → calculates accuracy metrics by topic and difficulty
3. **Rule engine applies if-then rules** → decides next action
4. **Returns decision**: QUESTION, LESSON, or FEEDBACK with appropriate difficulty level

### Example Usage

```python
from system import StudentPerformanceSystem

# Initialize system
system = StudentPerformanceSystem()

# Process a student answer
result = system.process_answer(
    student_id="student_001",
    question=my_question,
    student_answer="4",
    time_taken_seconds=5,
    current_topic="algebra"
)

# Check what to show next
print(result['next_action']['action'])  # 'question', 'lesson', or 'feedback'
print(result['next_action']['difficulty'])  # 'EASY', 'MEDIUM', or 'HARD'
```

### Rule-Based Logic

The system uses 9 explicit rules:
1. First-time students → Easy questions
2. 3+ consecutive failures → Show lesson
3. Low topic accuracy (<50%) → Show feedback
4. Recent performance decline → Intervention
5. Easy mastery (>90%) → Advance to medium
6. Medium mastery (>90%) → Advance to hard
7. Hard struggles (<50%) → Step back to medium
8. Good performance → Continue same level
9. Default → Adaptive difficulty

### License

See repository license.
