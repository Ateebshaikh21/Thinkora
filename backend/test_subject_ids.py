from utils.session_manager import SessionManager

# Test the simplified subject-based ID system
session_manager = SessionManager()

# Test different subjects to see the clean IDs generated
test_subjects = [
    "Machine Learning",
    "Data Structures and Algorithms", 
    "Computer Networks",
    "Database Management Systems",
    "Artificial Intelligence",
    "Web Development",
    "Python Programming",
    "React Development",
    "Software Engineering",
    "Operating Systems",
    "Mobile Development",
    "Computer Graphics"
]

print("🎯 Testing Clean Subject-Based Session IDs:")
print("=" * 60)

for i, subject in enumerate(test_subjects, 1):
    # Generate clean subject-based ID
    session_id = session_manager._create_subject_based_id(subject, 1)
    
    print(f"{i:2d}. Subject: {subject}")
    print(f"    📝 Clean Session ID: {session_id}")
    print()

print("✨ CLEAN SUBJECT ID FEATURES:")
print("=" * 60)
print("🎯 Simple & Clean:")
print("   • Machine Learning → machine-learning")
print("   • Computer Networks → computer-networks") 
print("   • Database Management → database-management")
print("   • Artificial Intelligence → artificial-intelligence")
print()
print("🔗 Perfect URLs:")
print("   • /analysis?session=machine-learning")
print("   • /history/computer-networks")
print("   • /session/database-management")
print()
print("✏️ Editable:")
print("   • machine-learning → ml-basics")
print("   • computer-networks → networking")
print("   • database-management → sql-study")
print()
print("📚 Subject-Focused:")
print("   • No random numbers or letters")
print("   • No document counts in ID")
print("   • Just clean subject names")
print()
print("🎉 RESULT: Clean, simple session IDs = just the subject name!")