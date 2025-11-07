from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List
import logging
from models.schemas import StudySession, UploadedDocument, QuestionSet
from database.db_connection import get_sessions_collection
from ai_engine.question_classifier import QuestionClassifier
from ai_engine.nlp_analysis import NLPAnalyzer
from utils.file_processor import FileProcessor
from utils.session_manager import session_manager
import uuid
from datetime import datetime

router = APIRouter()

@router.post("/upload-documents")
async def upload_documents(
    subject_id: str,
    files: List[UploadFile] = File(...),
    user_id: str = None
):
    """
    Upload and analyze study documents (PYQs, notes, syllabus)
    Supports: PDF, DOCX, XLSX, TXT, CSV, MD, RTF files
    """
    try:
        sessions_collection = get_sessions_collection()
        nlp_analyzer = NLPAnalyzer()
        
        uploaded_docs = []
        all_questions = []
        processing_errors = []
        
        for file in files:
            # Check if file format is supported
            if not FileProcessor.is_supported(file.filename):
                processing_errors.append(f"Unsupported file format: {file.filename}")
                continue
            
            # Read file content
            content = await file.read()
            
            # Extract text from file based on its format
            text_content, success = await FileProcessor.extract_text(content, file.filename)
            
            if not success:
                processing_errors.append(f"Failed to extract text from: {file.filename}")
                continue
            
            if not text_content.strip():
                processing_errors.append(f"No text content found in: {file.filename}")
                continue
            
            # Determine document type based on filename
            doc_type = _determine_document_type(file.filename)
            
            # Extract questions with marks from the document
            questions_with_marks = nlp_analyzer.extract_questions_from_text(text_content)
            all_questions.extend(questions_with_marks)
            
            uploaded_doc = UploadedDocument(
                filename=file.filename,
                content=text_content,
                document_type=doc_type
            )
            uploaded_docs.append(uploaded_doc)
        
        if not uploaded_docs:
            raise HTTPException(
                status_code=400, 
                detail=f"No documents could be processed. Errors: {'; '.join(processing_errors)}"
            )
        
        # Create study session
        study_session = StudySession(
            user_id=user_id,
            subject=subject_id,
            documents=uploaded_docs,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # Save session (try database first, fallback to file storage)
        if sessions_collection:
            try:
                session_dict = study_session.dict()
                session_dict["_id"] = str(uuid.uuid4())
                await sessions_collection.insert_one(session_dict)
                session_id = session_dict["_id"]
            except Exception as e:
                logging.warning(f"Database save failed, using file storage: {e}")
                session_id = session_manager.save_session(study_session)
        else:
            # Use file-based session storage
            try:
                session_id = session_manager.save_session(study_session)
                if not session_id:
                    raise HTTPException(status_code=500, detail="Failed to generate session ID")
            except Exception as e:
                logging.error(f"File storage save failed: {e}")
                raise HTTPException(status_code=500, detail=f"Failed to save session: {str(e)}")
        
        response = {
            "message": f"Successfully processed {len(uploaded_docs)} documents",
            "session_id": session_id,
            "documents_processed": len(uploaded_docs),
            "questions_extracted": len(all_questions),
            "document_types": [doc.document_type for doc in uploaded_docs],
            "supported_formats": FileProcessor.get_supported_extensions()
        }
        
        if processing_errors:
            response["warnings"] = processing_errors
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error uploading documents: {e}")
        raise HTTPException(status_code=500, detail="Failed to upload and analyze documents")

@router.post("/generate-questions/{session_id}")
async def generate_questions(session_id: str):
    """
    Generate categorized questions from uploaded documents
    """
    try:
        sessions_collection = get_sessions_collection()
        
        # Get study session (try database first, fallback to file storage)
        session = None
        
        if sessions_collection:
            try:
                session = await sessions_collection.find_one({"_id": session_id})
            except Exception as e:
                logging.warning(f"Database read failed, trying file storage: {e}")
        
        if not session:
            # Try file-based session storage
            session = session_manager.get_session(session_id)
            
        if not session:
            raise HTTPException(status_code=404, detail="Study session not found")
        
        # Initialize AI components
        nlp_analyzer = NLPAnalyzer()
        question_classifier = QuestionClassifier()
        
        # Extract all questions with marks from documents
        all_questions = []
        for doc in session["documents"]:
            questions_with_marks = nlp_analyzer.extract_questions_from_text(doc["content"])
            all_questions.extend(questions_with_marks)
        
        # Remove duplicates based on question text
        unique_questions = []
        seen_texts = set()
        for q in all_questions:
            if q['text'] not in seen_texts:
                unique_questions.append(q)
                seen_texts.add(q['text'])
        
        # Classify questions
        question_set = question_classifier.classify_questions(unique_questions)
        
        # Update session with generated questions
        question_set_dict = question_set.dict()
        
        if sessions_collection:
            try:
                await sessions_collection.update_one(
                    {"_id": session_id},
                    {
                        "$set": {
                            "question_set": question_set_dict,
                            "updated_at": datetime.now()
                        }
                    }
                )
            except Exception as e:
                logging.warning(f"Database update failed, using file storage: {e}")
                session_manager.update_session(session_id, {"question_set": question_set_dict})
        else:
            # Use file-based session storage
            session_manager.update_session(session_id, {"question_set": question_set_dict})
        
        return {
            "message": "Questions generated successfully",
            "session_id": session_id,
            "total_questions": len(unique_questions),
            "categorized_questions": {
                "frequent": len(question_set.frequent_questions),
                "moderate": len(question_set.moderate_questions),
                "important": len(question_set.important_questions),
                "predicted": len(question_set.predicted_questions)
            },
            "question_set": question_set.dict()
        }
        
    except Exception as e:
        logging.error(f"Error generating questions: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate questions")

@router.get("/session/{session_id}")
async def get_study_session(session_id: str):
    """
    Get study session details including generated questions
    """
    try:
        sessions_collection = get_sessions_collection()
        
        # Get study session (try database first, fallback to file storage)
        session = None
        
        if sessions_collection:
            try:
                session = await sessions_collection.find_one({"_id": session_id})
            except Exception as e:
                logging.warning(f"Database read failed, trying file storage: {e}")
        
        if not session:
            # Try file-based session storage
            session = session_manager.get_session(session_id)
            
        if not session:
            raise HTTPException(status_code=404, detail="Study session not found")
        
        return session
        
    except Exception as e:
        logging.error(f"Error retrieving session: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve study session")

@router.get("/sessions")
async def list_study_sessions(user_id: str = None, subject_id: str = None):
    """
    List all study sessions for a user or subject
    """
    try:
        sessions_collection = get_sessions_collection()
        
        # Get sessions (try database first, fallback to file storage)
        sessions = []
        
        if sessions_collection:
            try:
                query = {}
                if user_id:
                    query["user_id"] = user_id
                if subject_id:
                    query["subject"] = subject_id
                
                sessions = await sessions_collection.find(query).to_list(100)
            except Exception as e:
                logging.warning(f"Database read failed, trying file storage: {e}")
        
        if not sessions:
            # Use file-based session storage
            sessions = session_manager.list_sessions(user_id=user_id, subject=subject_id)
        
        return {"sessions": sessions}
        
    except Exception as e:
        logging.error(f"Error listing sessions: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve sessions")

@router.delete("/session/{session_id}")
async def delete_study_session(session_id: str):
    """
    Delete a study session
    """
    try:
        sessions_collection = get_sessions_collection()
        
        # Try database first
        if sessions_collection:
            try:
                result = await sessions_collection.delete_one({"_id": session_id})
                if result.deleted_count > 0:
                    return {"message": "Session deleted successfully"}
            except Exception as e:
                logging.warning(f"Database delete failed, trying file storage: {e}")
        
        # Try file-based session storage
        if session_manager.delete_session(session_id):
            return {"message": "Session deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Session not found")
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error deleting session: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete session")

@router.put("/session/{session_id}/rename")
async def rename_session(session_id: str, new_id: str):
    """
    Rename a session ID (change the session identifier)
    """
    try:
        sessions_collection = get_sessions_collection()
        
        # Validate new ID format
        if not new_id or len(new_id.strip()) == 0:
            raise HTTPException(status_code=400, detail="New session ID cannot be empty")
        
        # Clean the new ID
        clean_new_id = new_id.strip().lower().replace(' ', '-')
        clean_new_id = ''.join(c for c in clean_new_id if c.isalnum() or c == '-')
        clean_new_id = clean_new_id.strip('-')
        
        if not clean_new_id:
            raise HTTPException(status_code=400, detail="Invalid session ID format")
        
        # Create a clean display name from the new session ID
        clean_display_name = clean_new_id.replace('-', ' ').title()
        
        # Try database first
        if sessions_collection:
            try:
                # Check if new ID already exists
                existing = await sessions_collection.find_one({"_id": clean_new_id})
                if existing:
                    raise HTTPException(status_code=409, detail="Session ID already exists")
                
                # Get the session to rename
                session = await sessions_collection.find_one({"_id": session_id})
                if not session:
                    raise HTTPException(status_code=404, detail="Session not found")
                
                # Create new session with new ID and updated display name
                session["_id"] = clean_new_id
                session["id"] = clean_new_id
                session["display_name"] = clean_display_name
                session["updated_at"] = datetime.now()
                await sessions_collection.insert_one(session)
                
                # Delete old session
                await sessions_collection.delete_one({"_id": session_id})
                
                return {"message": "Session renamed successfully", "new_id": clean_new_id}
                
            except HTTPException:
                raise
            except Exception as e:
                logging.warning(f"Database rename failed, trying file storage: {e}")
        
        # Try file-based session storage
        if session_manager.update_session_id(session_id, clean_new_id):
            # Also update the display name in file storage
            session_manager.update_session(clean_new_id, {"display_name": clean_display_name})
            return {"message": "Session renamed successfully", "new_id": clean_new_id}
        else:
            raise HTTPException(status_code=404, detail="Session not found or ID already exists")
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error renaming session: {e}")
        raise HTTPException(status_code=500, detail="Failed to rename session")

def _determine_document_type(filename: str) -> str:
    """
    Determine document type based on filename
    """
    filename_lower = filename.lower()
    
    if any(keyword in filename_lower for keyword in ['pyq', 'previous', 'past', 'question']):
        return "pyq"
    elif any(keyword in filename_lower for keyword in ['note', 'lecture', 'chapter']):
        return "notes"
    elif any(keyword in filename_lower for keyword in ['syllabus', 'curriculum', 'outline']):
        return "syllabus"
    else:
        return "mixed"