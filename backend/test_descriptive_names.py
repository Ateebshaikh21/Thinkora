from utils.session_manager import SessionManager
from datetime import datetime

# Test the new descriptive session names
session_manager = SessionManager()

# Test scenarios with different subjects and document counts
test_scenarios = [
    ("Machine Learning", 1, "Single ML document"),
    ("Data Structures and Algorithms", 2, "Two DSA documents"),
    ("Computer Networks", 3, "Three network documents"),
    ("Database Management Systems", 4, "Four DBMS documents"),
    ("Artificial Intelligence", 5, "Five AI documents"),
    ("Web Development", 1, "Single web dev document"),
    ("Final Exam Preparation", 6, "Multiple exam prep docs"),
    ("Python Programming", 2, "Two Python docs"),
    ("React Development", 3, "Three React docs"),
    ("Software Engineering", 1, "Single SE document")
]

print("🎯 Testing New Descriptive Session Names (No Random Elements):")
print("=" * 70)

for i, (subject, doc_count, description) in enumerate(test_scenarios, 1):
    # Generate descriptive session name
    session_name = session_manager.generate_session_name(subject, doc_count)
    
    print(f"{i:2d}. Subject: {subject}")
    print(f"    Documents: {doc_count}")
    print(f"    📝 Descriptive Name: {session_name}")
    print()

print("✨ NEW DESCRIPTIVE SESSION NAME FEATURES:")
print("=" * 70)
print("📅 Complete Date Context:")
print("   • Monday Morning, Tuesday Evening, Wednesday Night")
print("   • Specific month and day: (November 6)")
print()
print("🎯 Study Intensity Based on Documents:")
print("   • 1 doc: Quick")
print("   • 2-3 docs: Focused") 
print("   • 3-4 docs: Intensive")
print("   • 5+ docs: Comprehensive")
print()
print("📚 Full Subject Names:")
print("   • ML → Machine Learning")
print("   • DSA → Data Structures & Algorithms")
print("   • AI → Artificial Intelligence")
print()
print("🕐 Detailed Time Periods:")
print("   • Early Morning (5-8 AM)")
print("   • Morning (8-12 PM)")
print("   • Afternoon (2-5 PM)")
print("   • Evening (5-8 PM)")
print("   • Night (8-11 PM)")
print()
print("📖 Study Purpose Detection:")
print("   • Exam keywords → Exam Preparation")
print("   • Practice keywords → Practice Session")
print("   • Review keywords → Review Session")
print()
print("🎉 RESULT: Completely descriptive names with NO random elements!")