from utils.session_manager import SessionManager
from models.schemas import StudySession, UploadedDocument

# Test the enhanced session name generation
session_manager = SessionManager()

# Test different subjects with various scenarios
test_scenarios = [
    ("Machine Learning", 2, "Standard ML course"),
    ("Data Structures and Algorithms", 1, "Single document DSA"),
    ("Computer Networks", 3, "Multiple network docs"),
    ("Database Management Systems", 1, "DBMS study material"),
    ("Artificial Intelligence", 4, "AI comprehensive study"),
    ("Software Engineering", 2, "SE project docs"),
    ("Web Development", 1, "Frontend learning"),
    ("Mobile App Development", 3, "Mobile dev resources"),
    ("Final Exam Preparation", 5, "Exam prep materials"),
    ("Quick Review Session", 1, "Last minute review")
]

print("🎯 Testing Enhanced Intelligent Session Names:")
print("=" * 60)

for i, (subject, doc_count, description) in enumerate(test_scenarios, 1):
    # Generate session name
    session_name = session_manager.generate_session_name(subject, doc_count)
    
    print(f"{i:2d}. Subject: {subject}")
    print(f"    Docs: {doc_count} | {description}")
    print(f"    📝 Session Name: {session_name}")
    print()

print("✨ NEW ENHANCED SESSION NAME FEATURES:")
print("=" * 60)
print("🕐 Time-Aware Adjectives:")
print("   • Morning: Fresh, Early, Productive, Focused, Energetic")
print("   • Afternoon: Intensive, Comprehensive, Detailed, Strategic")
print("   • Evening: Deep, Advanced, Complete, Expert, Master")
print("   • Night: Power, Elite, Pro, Smart, Efficient")
print()
print("🎯 Smart Subject Recognition:")
print("   • Machine Learning → ML")
print("   • Data Structures → DSA") 
print("   • Computer Networks → Networks")
print("   • Database Management → DBMS")
print()
print("📚 Context-Aware Activities:")
print("   • Exam keywords → Exam Prep, Final Review")
print("   • Practice keywords → Practice Round, Skill Building")
print("   • Review keywords → Review Session, Revision Marathon")
print()
print("📅 Readable Date Format:")
print("   • Old: 1106.2025")
print("   • New: Nov 6, 2:30 PM")
print()
print("🎉 RESULT: Beautiful, intelligent session names that make sense!")