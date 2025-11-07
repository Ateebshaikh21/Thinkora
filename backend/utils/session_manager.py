import json
import os
from typing import Dict, List, Optional
from datetime import datetime
from models.schemas import StudySession, UploadedDocument, QuestionSet
import uuid
import random

class SessionManager:
    """
    Simple file-based session storage for development when MongoDB is not available
    """
    
    def __init__(self, storage_dir: str = "sessions"):
        self.storage_dir = storage_dir
        self.ensure_storage_dir()
        
        # Descriptive session name components - no random elements
        self.time_descriptors = {
            'early_morning': "Early Morning",      # 5-8 AM
            'morning': "Morning",                  # 8-12 PM
            'midday': "Midday",                   # 12-2 PM
            'afternoon': "Afternoon",             # 2-5 PM
            'evening': "Evening",                 # 5-8 PM
            'night': "Night",                     # 8-11 PM
            'late_night': "Late Night"            # 11 PM-5 AM
        }
        
        self.study_intensities = {
            'light': "Quick",
            'moderate': "Focused", 
            'intensive': "Intensive",
            'comprehensive': "Comprehensive"
        }
        
        self.study_purposes = {
            'exam_prep': "Exam Preparation",
            'learning': "Learning Session",
            'practice': "Practice Session", 
            'review': "Review Session",
            'analysis': "Analysis Session",
            'research': "Research Session",
            'assignment': "Assignment Work",
            'project': "Project Work"
        }
        
        self.subject_full_names = {
            'machine learning': 'Machine Learning',
            'ml': 'Machine Learning',
            'artificial intelligence': 'Artificial Intelligence', 
            'ai': 'Artificial Intelligence',
            'data structures': 'Data Structures',
            'dsa': 'Data Structures & Algorithms',
            'algorithms': 'Algorithms',
            'computer networks': 'Computer Networks',
            'networking': 'Computer Networks',
            'database': 'Database Systems',
            'dbms': 'Database Management',
            'sql': 'Database Systems',
            'software engineering': 'Software Engineering',
            'software development': 'Software Development',
            'operating systems': 'Operating Systems',
            'os': 'Operating Systems',
            'computer graphics': 'Computer Graphics',
            'web development': 'Web Development',
            'frontend': 'Frontend Development',
            'backend': 'Backend Development',
            'mobile development': 'Mobile Development',
            'android': 'Android Development',
            'ios': 'iOS Development',
            'python': 'Python Programming',
            'java': 'Java Programming',
            'javascript': 'JavaScript Programming',
            'react': 'React Development',
            'node': 'Node.js Development'
        }
        
        self.weekday_names = {
            0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday",
            4: "Friday", 5: "Saturday", 6: "Sunday"
        }
        
        self.month_names = {
            1: "January", 2: "February", 3: "March", 4: "April",
            5: "May", 6: "June", 7: "July", 8: "August", 
            9: "September", 10: "October", 11: "November", 12: "December"
        }
    
    def ensure_storage_dir(self):
        """Create storage directory if it doesn't exist"""
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)
    
    def generate_session_name(self, subject: str, document_count: int = 0) -> str:
        """Generate a completely descriptive session name without random elements"""
        now = datetime.now()
        
        # Get descriptive time period
        time_descriptor = self._get_time_descriptor(now)
        
        # Get descriptive weekday and date
        weekday = self.weekday_names[now.weekday()]
        month = self.month_names[now.month]
        day = now.day
        
        # Process subject to full descriptive name
        subject_name = self._get_full_subject_name(subject)
        
        # Determine study purpose based on context
        study_purpose = self._determine_study_purpose(subject, document_count)
        
        # Determine intensity based on document count and time
        intensity = self._determine_study_intensity(document_count, now)
        
        # Create descriptive document context
        doc_context = self._get_descriptive_document_context(document_count)
        
        # Build the complete descriptive name
        name_parts = []
        
        # Add time and day context
        name_parts.append(f"{weekday} {time_descriptor}")
        
        # Add intensity and purpose
        name_parts.append(f"{intensity} {study_purpose}")
        
        # Add subject
        if subject_name:
            name_parts.append(f"in {subject_name}")
        
        # Add document context if relevant
        if doc_context:
            name_parts.append(doc_context)
        
        # Add specific date for uniqueness
        name_parts.append(f"({month} {day})")
        
        return " ".join(name_parts)
    
    def _get_time_descriptor(self, now: datetime) -> str:
        """Get descriptive time period"""
        hour = now.hour
        
        if 5 <= hour < 8:
            return self.time_descriptors['early_morning']
        elif 8 <= hour < 12:
            return self.time_descriptors['morning']
        elif 12 <= hour < 14:
            return self.time_descriptors['midday']
        elif 14 <= hour < 17:
            return self.time_descriptors['afternoon']
        elif 17 <= hour < 20:
            return self.time_descriptors['evening']
        elif 20 <= hour < 23:
            return self.time_descriptors['night']
        else:
            return self.time_descriptors['late_night']
    
    def _get_full_subject_name(self, subject: str) -> str:
        """Convert subject to full descriptive name"""
        if not subject:
            return ""
        
        subject_lower = subject.lower().strip()
        
        # Check for exact matches first
        if subject_lower in self.subject_full_names:
            return self.subject_full_names[subject_lower]
        
        # Check for partial matches
        for key, full_name in self.subject_full_names.items():
            if key in subject_lower or subject_lower in key:
                return full_name
        
        # If no match, clean up the original subject
        return self._clean_subject_name(subject)
    
    def _clean_subject_name(self, subject: str) -> str:
        """Clean and format subject name"""
        # Split into words and capitalize each
        words = subject.split()
        cleaned_words = []
        
        skip_words = {'and', 'the', 'of', 'in', 'to', 'for', 'with', 'on', 'at', 'by'}
        
        for word in words:
            clean_word = word.strip().replace('-', ' ').replace('_', ' ')
            if clean_word.lower() not in skip_words and len(clean_word) > 1:
                cleaned_words.append(clean_word.title())
        
        return ' '.join(cleaned_words)
    
    def _determine_study_purpose(self, subject: str, document_count: int) -> str:
        """Determine the purpose of the study session"""
        if not subject:
            return self.study_purposes['learning']
        
        subject_lower = subject.lower()
        
        # Check for specific keywords
        if any(word in subject_lower for word in ['exam', 'test', 'final', 'midterm', 'quiz']):
            return self.study_purposes['exam_prep']
        elif any(word in subject_lower for word in ['practice', 'exercise', 'problem', 'coding']):
            return self.study_purposes['practice']
        elif any(word in subject_lower for word in ['review', 'revision', 'recap']):
            return self.study_purposes['review']
        elif any(word in subject_lower for word in ['research', 'investigation', 'exploration']):
            return self.study_purposes['research']
        elif any(word in subject_lower for word in ['assignment', 'homework', 'task']):
            return self.study_purposes['assignment']
        elif any(word in subject_lower for word in ['project', 'development', 'implementation']):
            return self.study_purposes['project']
        else:
            return self.study_purposes['learning']
    
    def _determine_study_intensity(self, document_count: int, now: datetime) -> str:
        """Determine study intensity based on context"""
        hour = now.hour
        
        # Base intensity on document count
        if document_count >= 5:
            base_intensity = 'comprehensive'
        elif document_count >= 3:
            base_intensity = 'intensive'
        elif document_count >= 2:
            base_intensity = 'moderate'
        else:
            base_intensity = 'light'
        
        # Adjust based on time of day
        if hour < 8 or hour > 22:  # Early morning or late night
            if base_intensity == 'comprehensive':
                base_intensity = 'intensive'
            elif base_intensity == 'intensive':
                base_intensity = 'moderate'
        
        return self.study_intensities[base_intensity]
    
    def _get_descriptive_document_context(self, document_count: int) -> str:
        """Get descriptive context about documents"""
        if document_count == 0:
            return ""
        elif document_count == 1:
            return "with Single Document"
        elif document_count == 2:
            return "with Two Documents"
        elif document_count == 3:
            return "with Three Documents"
        elif document_count == 4:
            return "with Four Documents"
        elif document_count == 5:
            return "with Five Documents"
        elif document_count <= 10:
            return f"with {document_count} Documents"
        else:
            return "with Multiple Documents"
    
    def _determine_activity_type(self, subject: str, time_context: str) -> str:
        """Determine the type of study activity based on subject and time"""
        if not subject:
            return 'default'
        
        subject_lower = subject.lower()
        
        # Check for exam-related keywords
        if any(word in subject_lower for word in ['exam', 'test', 'final', 'midterm']):
            return 'exam_prep'
        
        # Check for practice-related keywords
        if any(word in subject_lower for word in ['practice', 'exercise', 'problem', 'coding']):
            return 'practice'
        
        # Check for review-related keywords
        if any(word in subject_lower for word in ['review', 'revision', 'recap']):
            return 'review'
        
        # Time-based activity selection
        if time_context in ['morning', 'afternoon']:
            return 'learning'
        elif time_context == 'evening':
            return 'analysis'
        else:  # night
            return 'review'
    
    def _process_subject_name(self, subject: str) -> str:
        """Process subject name to create a clean, readable format"""
        if not subject:
            return ""
        
        subject_lower = subject.lower().strip()
        
        # Check for known subject patterns and use abbreviations
        for key, abbreviations in self.subject_keywords.items():
            if key in subject_lower:
                return abbreviations[0]  # Use the first (most common) abbreviation
        
        # Clean and format the subject name
        # Remove common words and clean up
        words = subject.split()
        cleaned_words = []
        
        skip_words = {'and', 'the', 'of', 'in', 'to', 'for', 'with', 'on', 'at', 'by'}
        
        for word in words:
            clean_word = word.strip().replace('-', '').replace('_', '')
            if clean_word.lower() not in skip_words and len(clean_word) > 1:
                # Capitalize first letter
                cleaned_words.append(clean_word.capitalize())
        
        # Join words and limit length
        result = ' '.join(cleaned_words)
        if len(result) > 20:
            # Take first two words or truncate
            if len(cleaned_words) >= 2:
                result = ' '.join(cleaned_words[:2])
            else:
                result = result[:20]
        
        return result
    
    def _format_document_info(self, document_count: int) -> str:
        """Format document count information"""
        if document_count == 0:
            return ""
        elif document_count == 1:
            return "(1 Doc)"
        elif document_count <= 5:
            return f"({document_count} Docs)"
        else:
            return "(Multi-Doc)"
    
    def _generate_smart_suffix(self, now: datetime) -> str:
        """Generate a smart, readable date/time suffix"""
        # Format: "Nov 6, 2:30 PM" or "Nov 6 Evening" for better readability
        date_part = now.strftime("%b %d")
        
        hour = now.hour
        if 5 <= hour < 12:
            time_part = "Morning"
        elif 12 <= hour < 17:
            time_part = "Afternoon"  
        elif 17 <= hour < 21:
            time_part = "Evening"
        else:
            time_part = "Night"
        
        # Add specific time for uniqueness
        time_specific = now.strftime("%I:%M %p")
        
        return f"{date_part}, {time_specific}"
    
    def _create_safe_filename(self, session_name: str) -> str:
        """Create a safe filename from session name by removing invalid characters"""
        # Characters that are invalid in Windows filenames
        invalid_chars = ['<', '>', ':', '"', '|', '?', '*', '/', '\\', ',']
        
        # Replace invalid characters with safe alternatives
        safe_name = session_name
        for char in invalid_chars:
            safe_name = safe_name.replace(char, '_')
        
        # Replace spaces with underscores
        safe_name = safe_name.replace(' ', '_')
        
        # Remove parentheses and other special characters
        safe_name = safe_name.replace('(', '').replace(')', '')
        safe_name = safe_name.replace('[', '').replace(']', '')
        
        # Replace multiple underscores with single underscore
        while '__' in safe_name:
            safe_name = safe_name.replace('__', '_')
        
        # Remove leading/trailing underscores
        safe_name = safe_name.strip('_')
        
        # Limit length to avoid filesystem issues
        if len(safe_name) > 100:
            safe_name = safe_name[:100]
        
        # Ensure it's not empty
        if not safe_name:
            safe_name = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        return safe_name
    
    def _create_subject_based_id(self, subject: str, document_count: int = 0) -> str:
        """Create a subject-based ID that's meaningful and editable"""
        if not subject:
            subject = "General_Study"
        
        # Clean subject for ID use
        subject_clean = subject.lower().strip()
        
        # Convert common subjects to short, meaningful IDs
        subject_mappings = {
            'machine learning': 'machine-learning',
            'ml': 'machine-learning',
            'artificial intelligence': 'artificial-intelligence',
            'ai': 'artificial-intelligence',
            'data structures': 'data-structures',
            'data structures and algorithms': 'data-structures-algorithms',
            'dsa': 'data-structures-algorithms',
            'computer networks': 'computer-networks',
            'networking': 'computer-networks',
            'database management': 'database-management',
            'database management systems': 'database-management',
            'dbms': 'database-management',
            'software engineering': 'software-engineering',
            'operating systems': 'operating-systems',
            'os': 'operating-systems',
            'web development': 'web-development',
            'frontend development': 'frontend-development',
            'backend development': 'backend-development',
            'mobile development': 'mobile-development',
            'computer graphics': 'computer-graphics',
            'python programming': 'python-programming',
            'java programming': 'java-programming',
            'javascript': 'javascript-programming',
            'react development': 'react-development',
            'node.js': 'nodejs-development'
        }
        
        # Check for direct mapping
        if subject_clean in subject_mappings:
            base_id = subject_mappings[subject_clean]
        else:
            # Create ID from subject name
            # Remove special characters and replace spaces with hyphens
            base_id = subject_clean.replace(' ', '-').replace('_', '-')
            base_id = ''.join(c for c in base_id if c.isalnum() or c == '-')
            # Remove multiple consecutive hyphens
            while '--' in base_id:
                base_id = base_id.replace('--', '-')
            base_id = base_id.strip('-')
        
        # Keep it simple - just the subject name
        # If this ID already exists, add a number suffix
        potential_id = base_id
        counter = 2
        while os.path.exists(os.path.join(self.storage_dir, f"{potential_id}.json")):
            potential_id = f"{base_id}-{counter}"
            counter += 1
        
        return potential_id
    
    def update_session_id(self, old_id: str, new_id: str) -> bool:
        """Update session ID (rename session)"""
        old_file = os.path.join(self.storage_dir, f"{old_id}.json")
        new_file = os.path.join(self.storage_dir, f"{new_id}.json")
        
        # Check if old file exists
        if not os.path.exists(old_file):
            return False
        
        # Check if new ID is already taken
        if os.path.exists(new_file):
            return False
        
        try:
            # Read the session data
            session = self.get_session(old_id)
            if not session:
                return False
            
            # Update the ID and display name in the session data
            session['id'] = new_id
            # Create a clean display name from the new ID
            clean_display_name = new_id.replace('-', ' ').title()
            session['display_name'] = clean_display_name
            session['updated_at'] = datetime.now()
            
            # Save with new ID
            session_copy = session.copy()
            session_copy["created_at"] = session_copy["created_at"].isoformat() if session_copy["created_at"] else None
            session_copy["updated_at"] = session_copy["updated_at"].isoformat() if session_copy["updated_at"] else None
            
            with open(new_file, 'w', encoding='utf-8') as f:
                json.dump(session_copy, f, indent=2, ensure_ascii=False)
            
            # Delete old file
            os.remove(old_file)
            
            return True
        except Exception as e:
            print(f"Error updating session ID from {old_id} to {new_id}: {e}")
            return False
    
    def save_session(self, session: StudySession) -> str:
        """Save session to file and return session ID"""
        if not session.id:
            # Generate meaningful session name for display
            document_count = len(session.documents) if session.documents else 0
            session_name = self.generate_session_name(session.subject, document_count)
            
            # Set display name for UI
            session.display_name = session_name
            
            # Create subject-based ID that's editable
            session.id = self._create_subject_based_id(session.subject, document_count)
        
        session_file = os.path.join(self.storage_dir, f"{session.id}.json")
        
        # Convert to dict and handle datetime serialization
        session_dict = session.dict()
        session_dict["created_at"] = session_dict["created_at"].isoformat() if session_dict["created_at"] else None
        session_dict["updated_at"] = session_dict["updated_at"].isoformat() if session_dict["updated_at"] else None
        
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(session_dict, f, indent=2, ensure_ascii=False)
        
        return session.id
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """Get session by ID"""
        session_file = os.path.join(self.storage_dir, f"{session_id}.json")
        
        if not os.path.exists(session_file):
            return None
        
        try:
            with open(session_file, 'r', encoding='utf-8') as f:
                session_dict = json.load(f)
            
            # Convert datetime strings back to datetime objects
            if session_dict.get("created_at"):
                session_dict["created_at"] = datetime.fromisoformat(session_dict["created_at"])
            if session_dict.get("updated_at"):
                session_dict["updated_at"] = datetime.fromisoformat(session_dict["updated_at"])
            
            return session_dict
        except Exception as e:
            print(f"Error loading session {session_id}: {e}")
            return None
    
    def update_session(self, session_id: str, updates: Dict) -> bool:
        """Update session with new data"""
        session = self.get_session(session_id)
        if not session:
            return False
        
        # Update the session data
        session.update(updates)
        session["updated_at"] = datetime.now()
        
        # Save back to file
        session_file = os.path.join(self.storage_dir, f"{session_id}.json")
        
        # Handle datetime serialization
        session_copy = session.copy()
        session_copy["created_at"] = session_copy["created_at"].isoformat() if session_copy["created_at"] else None
        session_copy["updated_at"] = session_copy["updated_at"].isoformat() if session_copy["updated_at"] else None
        
        try:
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(session_copy, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error updating session {session_id}: {e}")
            return False
    
    def list_sessions(self, user_id: Optional[str] = None, subject: Optional[str] = None) -> List[Dict]:
        """List all sessions, optionally filtered by user_id or subject"""
        sessions = []
        
        if not os.path.exists(self.storage_dir):
            return sessions
        
        for filename in os.listdir(self.storage_dir):
            if filename.endswith('.json'):
                session_id = filename[:-5]  # Remove .json extension
                session = self.get_session(session_id)
                
                if session:
                    # Apply filters
                    if user_id and session.get("user_id") != user_id:
                        continue
                    if subject and session.get("subject") != subject:
                        continue
                    
                    sessions.append(session)
        
        # Sort by updated_at (most recent first)
        sessions.sort(key=lambda x: x.get("updated_at", datetime.min), reverse=True)
        return sessions
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session"""
        session_file = os.path.join(self.storage_dir, f"{session_id}.json")
        
        if os.path.exists(session_file):
            try:
                os.remove(session_file)
                return True
            except Exception as e:
                print(f"Error deleting session {session_id}: {e}")
                return False
        return False

# Global session manager instance
session_manager = SessionManager()