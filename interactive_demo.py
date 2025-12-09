"""
Interactive demonstration of the rule-based student performance system.
Shows how the system analyzes and adapts to different student behaviors.
"""
from system import StudentPerformanceSystem, create_sample_questions
from models import DifficultyLevel


def print_header(text):
    """Print a formatted header."""
    print("\n" + "="*80)
    print(f"  {text}")
    print("="*80)


def print_decision_box(decision):
    """Print a formatted decision box."""
    print("\n┌" + "─"*78 + "┐")
    print(f"│ SYSTEM DECISION: {decision['action'].upper():60} │")
    print("├" + "─"*78 + "┤")
    if decision.get('difficulty'):
        print(f"│ Difficulty: {decision['difficulty']:65} │")
    print(f"│ Reason: {decision['reason']:69} │")
    print(f"│ Message: {decision['message'][:68]:68} │")
    print("└" + "─"*78 + "┘")


def simulate_learning_journey():
    """Simulate a complete learning journey."""
    print_header("STUDENT LEARNING JOURNEY SIMULATION")
    
    system = StudentPerformanceSystem()
    questions = create_sample_questions()
    student_id = "demo_student"
    topic = "algebra"
    
    # Phase 1: Getting Started
    print("\n📚 PHASE 1: Getting Started")
    print("-" * 80)
    
    next_action = system.get_next_action_for_student(student_id, topic)
    print(f"\n👤 New student '{student_id}' begins learning '{topic}'")
    print_decision_box(next_action)
    
    # Phase 2: Initial Success
    print("\n\n📚 PHASE 2: Initial Success")
    print("-" * 80)
    
    for i in range(3):
        result = system.process_answer(
            student_id=student_id,
            question=questions[0],
            student_answer="4",
            time_taken_seconds=5 + i,
            current_topic=topic
        )
        print(f"\n✓ Question {i+1}: CORRECT (in {5+i}s)")
    
    perf = system.get_student_summary(student_id)
    print(f"\n📊 Performance: {perf['correct_attempts']}/{perf['total_attempts']} correct ({perf['overall_accuracy']:.0f}%)")
    
    next_action = system.get_next_action_for_student(student_id, topic)
    print_decision_box(next_action)
    
    # Phase 3: Hitting a Challenge
    print("\n\n📚 PHASE 3: Facing Challenges")
    print("-" * 80)
    
    # Try medium questions with mixed results
    results_pattern = ["3", "wrong", "3", "wrong"]
    for i, answer in enumerate(results_pattern):
        result = system.process_answer(
            student_id=student_id,
            question=questions[2],  # Medium question
            student_answer=answer,
            time_taken_seconds=15,
            current_topic=topic
        )
        status = "✓" if result['attempt']['is_correct'] else "✗"
        print(f"{status} Question {i+4}: {'CORRECT' if result['attempt']['is_correct'] else 'INCORRECT'} (in 15s)")
    
    perf = system.get_student_summary(student_id)
    print(f"\n📊 Performance: {perf['correct_attempts']}/{perf['total_attempts']} correct ({perf['overall_accuracy']:.0f}%)")
    
    next_action = system.get_next_action_for_student(student_id, topic)
    print_decision_box(next_action)
    
    # Phase 4: Struggling
    print("\n\n📚 PHASE 4: Struggling & Intervention")
    print("-" * 80)
    
    # Three consecutive wrong answers
    for i in range(3):
        result = system.process_answer(
            student_id=student_id,
            question=questions[3],  # Hard question
            student_answer="wrong",
            time_taken_seconds=30,
            current_topic=topic
        )
        print(f"✗ Question {i+8}: INCORRECT (struggled for 30s)")
    
    perf = system.get_student_summary(student_id)
    print(f"\n📊 Performance: {perf['correct_attempts']}/{perf['total_attempts']} correct ({perf['overall_accuracy']:.0f}%)")
    print("⚠️  Recent performance shows struggle - triggering intervention...")
    
    next_action = system.get_next_action_for_student(student_id, topic)
    print_decision_box(next_action)
    
    # Final Summary
    print("\n\n📊 FINAL LEARNING ANALYTICS")
    print("="*80)
    
    summary = system.get_student_summary(student_id)
    
    print(f"\nOverall Statistics:")
    print(f"  • Total Attempts: {summary['total_attempts']}")
    print(f"  • Correct Answers: {summary['correct_attempts']}")
    print(f"  • Overall Accuracy: {summary['overall_accuracy']:.1f}%")
    print(f"  • Average Time: {summary['average_time_seconds']:.1f} seconds")
    
    print(f"\nPerformance by Difficulty:")
    for level, accuracy in summary['difficulty_accuracy'].items():
        bar = "█" * int(accuracy / 5)
        print(f"  • {level.upper():8} {bar:20} {accuracy:.1f}%")
    
    print(f"\nLast 5 Attempts:")
    for i, attempt in enumerate(summary['recent_attempts'][-5:], 1):
        status = "✓" if attempt['is_correct'] else "✗"
        print(f"  {status} {attempt['difficulty']:6} - {attempt['time_taken']:2}s")
    
    print("\n" + "="*80)
    print("✅ Learning journey simulation complete!")
    print("="*80)


def show_rule_engine_logic():
    """Display the rule engine logic."""
    print_header("RULE ENGINE LOGIC")
    
    print("\nThe system uses 9 explicit if-then rules:\n")
    
    rules = [
        ("Rule 1", "IF student has no attempts", "THEN show EASY question"),
        ("Rule 2", "IF 3+ consecutive incorrect", "THEN show LESSON"),
        ("Rule 3", "IF topic accuracy < 50%", "THEN show FEEDBACK"),
        ("Rule 4", "IF recent performance declining", "THEN provide intervention"),
        ("Rule 5", "IF easy accuracy >= 90%", "THEN advance to MEDIUM"),
        ("Rule 6", "IF medium accuracy >= 90%", "THEN advance to HARD"),
        ("Rule 7", "IF hard accuracy < 50%", "THEN step back to MEDIUM"),
        ("Rule 8", "IF good overall performance", "THEN continue same level"),
        ("Rule 9", "DEFAULT", "THEN adaptive difficulty")
    ]
    
    for rule_name, condition, action in rules:
        print(f"  {rule_name:8} {condition:35} → {action}")
    
    print("\n" + "="*80)


def show_data_model():
    """Show the labeled data model."""
    print_header("LABELED DATA MODEL")
    
    print("\nEach student attempt is labeled with:")
    print("  • Correctness: Binary (True/False)")
    print("  • Difficulty: Categorical (EASY/MEDIUM/HARD)")
    print("  • Topic: String (algebra, geometry, etc.)")
    print("  • Time Taken: Integer (seconds)")
    print("  • Timestamp: DateTime")
    
    print("\nThis labeled data enables:")
    print("  ✓ Supervised learning approach")
    print("  ✓ Performance tracking by topic & difficulty")
    print("  ✓ Trend analysis (improving/declining)")
    print("  ✓ Personalized recommendations")
    
    print("\n" + "="*80)


if __name__ == "__main__":
    print("\n" + "█"*80)
    print("█" + " "*78 + "█")
    print("█" + "  RULE-BASED STUDENT PERFORMANCE ANALYSIS SYSTEM".center(78) + "█")
    print("█" + "  Interactive Demonstration".center(78) + "█")
    print("█" + " "*78 + "█")
    print("█"*80)
    
    # Show all demonstrations
    show_rule_engine_logic()
    show_data_model()
    simulate_learning_journey()
    
    print("\n🎓 System demonstrates:")
    print("  ✓ Rule-based supervised decision making")
    print("  ✓ Labeled data collection and analysis")
    print("  ✓ Adaptive difficulty progression")
    print("  ✓ Intelligent intervention triggers")
    print("  ✓ Comprehensive performance analytics\n")
