"""
Comprehensive example demonstrating the rule-based student performance system.
"""
from system import StudentPerformanceSystem, create_sample_questions
from models import Question, DifficultyLevel


def print_separator(title=""):
    """Print a nice separator."""
    if title:
        print(f"\n{'='*70}")
        print(f"  {title}")
        print('='*70)
    else:
        print('-'*70)


def demonstrate_first_time_student():
    """Demonstrate system behavior for a first-time student."""
    print_separator("SCENARIO 1: First-Time Student")
    
    system = StudentPerformanceSystem()
    questions = create_sample_questions()
    
    student_id = "new_student"
    topic = "algebra"
    
    # Get recommendation for first question
    next_action = system.get_next_action_for_student(student_id, topic)
    
    print(f"\nStudent: {student_id} (New Student)")
    print(f"Topic: {topic}")
    print(f"\nSystem Decision:")
    print(f"  Action: {next_action['action']}")
    print(f"  Difficulty: {next_action['difficulty']}")
    print(f"  Reason: {next_action['reason']}")
    print(f"  Message: {next_action['message']}")


def demonstrate_progression():
    """Demonstrate difficulty progression based on performance."""
    print_separator("SCENARIO 2: Difficulty Progression")
    
    system = StudentPerformanceSystem()
    questions = create_sample_questions()
    
    student_id = "progressing_student"
    topic = "algebra"
    
    print(f"\nStudent: {student_id}")
    print(f"Topic: {topic}")
    
    # Student answers 5 easy questions correctly
    print("\n--- Answering 5 Easy Questions Correctly ---")
    for i in range(5):
        result = system.process_answer(
            student_id=student_id,
            question=questions[0],  # Easy question
            student_answer="4",  # Correct answer
            time_taken_seconds=5,
            current_topic=topic
        )
        print(f"  Question {i+1}: Correct")
    
    # Check what system recommends next
    next_action = system.get_next_action_for_student(student_id, topic)
    
    print(f"\nAfter 5 correct easy answers:")
    print(f"  Next Action: {next_action['action']}")
    print(f"  Difficulty: {next_action['difficulty']}")
    print(f"  Reason: {next_action['reason']}")
    print(f"  Overall Accuracy: {next_action['performance']['overall_accuracy']:.1f}%")


def demonstrate_struggling_student():
    """Demonstrate intervention for struggling students."""
    print_separator("SCENARIO 3: Struggling Student - Intervention")
    
    system = StudentPerformanceSystem()
    questions = create_sample_questions()
    
    student_id = "struggling_student"
    topic = "algebra"
    
    print(f"\nStudent: {student_id}")
    print(f"Topic: {topic}")
    
    # Student gets 3 consecutive wrong answers
    print("\n--- Answering 3 Questions Incorrectly ---")
    for i in range(3):
        result = system.process_answer(
            student_id=student_id,
            question=questions[0],
            student_answer="wrong",  # Incorrect answer
            time_taken_seconds=15,
            current_topic=topic
        )
        print(f"  Question {i+1}: Incorrect")
    
    # Check system recommendation
    next_action = system.get_next_action_for_student(student_id, topic)
    
    print(f"\nAfter 3 consecutive incorrect answers:")
    print(f"  Next Action: {next_action['action']}")
    print(f"  Reason: {next_action['reason']}")
    print(f"  Message: {next_action['message']}")


def demonstrate_mixed_performance():
    """Demonstrate system handling mixed performance."""
    print_separator("SCENARIO 4: Mixed Performance")
    
    system = StudentPerformanceSystem()
    questions = create_sample_questions()
    
    student_id = "mixed_student"
    topic = "algebra"
    
    print(f"\nStudent: {student_id}")
    print(f"Topic: {topic}")
    
    # Alternate between correct and incorrect
    answers = ["4", "wrong", "15", "wrong", "4", "15", "wrong", "4"]
    correct_answers = ["4", "4", "15", "15", "4", "15", "15", "4"]
    
    print("\n--- Mixed Performance Pattern ---")
    correct_count = 0
    for i, (answer, correct) in enumerate(zip(answers, correct_answers)):
        is_correct = (answer == correct)
        if is_correct:
            correct_count += 1
        
        result = system.process_answer(
            student_id=student_id,
            question=questions[i % len(questions)],
            student_answer=answer,
            time_taken_seconds=10,
            current_topic=topic
        )
        status = "✓" if is_correct else "✗"
        print(f"  Question {i+1}: {status}")
    
    # Get summary
    summary = system.get_student_summary(student_id)
    
    print(f"\nPerformance Summary:")
    print(f"  Total Attempts: {summary['total_attempts']}")
    print(f"  Correct: {summary['correct_attempts']}/{summary['total_attempts']}")
    print(f"  Overall Accuracy: {summary['overall_accuracy']:.1f}%")
    print(f"  Topic Accuracy: {summary['topic_accuracy']}")
    
    # Get next recommendation
    next_action = system.get_next_action_for_student(student_id, topic)
    print(f"\nNext Recommendation:")
    print(f"  Action: {next_action['action']}")
    print(f"  Difficulty: {next_action['difficulty']}")
    print(f"  Message: {next_action['message']}")


def demonstrate_multiple_topics():
    """Demonstrate tracking across multiple topics."""
    print_separator("SCENARIO 5: Multiple Topics")
    
    system = StudentPerformanceSystem()
    questions = create_sample_questions()
    
    student_id = "multi_topic_student"
    
    print(f"\nStudent: {student_id}")
    
    # Good at algebra
    print("\n--- Algebra Performance (Good) ---")
    for i in range(3):
        result = system.process_answer(
            student_id=student_id,
            question=questions[0],  # Algebra question
            student_answer="4",
            time_taken_seconds=5,
            current_topic="algebra"
        )
        print(f"  Question {i+1}: Correct")
    
    # Struggling with geometry
    print("\n--- Geometry Performance (Struggling) ---")
    for i in range(3):
        result = system.process_answer(
            student_id=student_id,
            question=questions[4],  # Geometry question
            student_answer="wrong",
            time_taken_seconds=15,
            current_topic="geometry"
        )
        print(f"  Question {i+1}: Incorrect")
    
    # Check recommendations for each topic
    summary = system.get_student_summary(student_id)
    
    print(f"\nOverall Performance:")
    print(f"  Total Attempts: {summary['total_attempts']}")
    print(f"  Overall Accuracy: {summary['overall_accuracy']:.1f}%")
    print(f"  Topic Breakdown:")
    for topic, accuracy in summary['topic_accuracy'].items():
        print(f"    {topic}: {accuracy:.1f}%")
    
    # Recommendations per topic
    print("\nRecommendations by Topic:")
    for topic in ["algebra", "geometry"]:
        next_action = system.get_next_action_for_student(student_id, topic)
        print(f"\n  {topic.upper()}:")
        print(f"    Action: {next_action['action']}")
        print(f"    Reason: {next_action['reason']}")


def demonstrate_detailed_analysis():
    """Demonstrate detailed performance analysis."""
    print_separator("SCENARIO 6: Detailed Performance Analysis")
    
    system = StudentPerformanceSystem()
    questions = create_sample_questions()
    
    student_id = "analyzed_student"
    topic = "algebra"
    
    print(f"\nStudent: {student_id}")
    print(f"Building performance history...")
    
    # Create a varied performance history
    test_cases = [
        (questions[0], "4", DifficultyLevel.EASY, True),
        (questions[1], "15", DifficultyLevel.EASY, True),
        (questions[2], "3", DifficultyLevel.MEDIUM, True),
        (questions[2], "wrong", DifficultyLevel.MEDIUM, False),
        (questions[3], "2 or 3", DifficultyLevel.HARD, True),
        (questions[3], "wrong", DifficultyLevel.HARD, False),
    ]
    
    for q, ans, diff, _ in test_cases:
        system.process_answer(
            student_id=student_id,
            question=q,
            student_answer=ans,
            time_taken_seconds=10,
            current_topic=topic
        )
    
    # Get comprehensive summary
    summary = system.get_student_summary(student_id)
    
    print(f"\nComprehensive Analysis:")
    print(f"  Total Attempts: {summary['total_attempts']}")
    print(f"  Overall Accuracy: {summary['overall_accuracy']:.1f}%")
    
    print(f"\n  Accuracy by Difficulty:")
    for level, accuracy in summary['difficulty_accuracy'].items():
        print(f"    {level.upper()}: {accuracy:.1f}%")
    
    print(f"\n  Recent Attempts:")
    for i, attempt in enumerate(summary['recent_attempts'][-5:], 1):
        status = "✓" if attempt['is_correct'] else "✗"
        print(f"    {i}. {attempt['difficulty']} - {status} ({attempt['time_taken']}s)")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("  RULE-BASED STUDENT PERFORMANCE ANALYSIS SYSTEM")
    print("  Comprehensive Demonstration")
    print("="*70)
    
    # Run all demonstrations
    demonstrate_first_time_student()
    demonstrate_progression()
    demonstrate_struggling_student()
    demonstrate_mixed_performance()
    demonstrate_multiple_topics()
    demonstrate_detailed_analysis()
    
    print_separator()
    print("\n✓ All scenarios demonstrated successfully!")
    print("\nKey Features Demonstrated:")
    print("  • Rule-based decision making (if-then logic)")
    print("  • Labeled data tracking (correctness, difficulty, topics)")
    print("  • Adaptive difficulty progression")
    print("  • Intervention for struggling students")
    print("  • Multi-topic performance tracking")
    print("  • Comprehensive performance analytics")
    print()
