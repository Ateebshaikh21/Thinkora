from fastapi import APIRouter, HTTPException
from models.schemas import SubjectRequest
from database.db_connection import get_subjects_collection
import logging

router = APIRouter()

@router.post("/setup")
async def setup_subject(subject_request: SubjectRequest):
    """
    Set up a new subject for study session
    """
    try:
        subjects_collection = get_subjects_collection()
        
        # If database is not available, return a mock response for development
        if subjects_collection is None:
            import uuid
            mock_id = str(uuid.uuid4())
            return {
                "message": f"Subject '{subject_request.subject_name}' set up successfully (Development Mode)",
                "subject_id": mock_id,
                "subject_name": subject_request.subject_name,
                "ai_context": f"Act as an expert in {subject_request.subject_name} for all further responses. Provide detailed, exam-focused explanations."
            }
        
        # Check if subject already exists for this user
        existing_subject = await subjects_collection.find_one({
            "name": subject_request.subject_name.lower(),
            "user_id": subject_request.user_id
        })
        
        if existing_subject:
            return {
                "message": f"Subject '{subject_request.subject_name}' already exists",
                "subject_id": str(existing_subject["_id"]),
                "subject_name": subject_request.subject_name
            }
        
        # Create new subject entry
        subject_doc = {
            "name": subject_request.subject_name.lower(),
            "display_name": subject_request.subject_name,
            "user_id": subject_request.user_id,
            "ai_context": f"Act as an expert in {subject_request.subject_name} for all further responses. Provide detailed, exam-focused explanations.",
            "created_at": None,  # Will be set by MongoDB
            "documents_count": 0,
            "questions_generated": 0
        }
        
        result = await subjects_collection.insert_one(subject_doc)
        
        return {
            "message": f"Subject '{subject_request.subject_name}' set up successfully",
            "subject_id": str(result.inserted_id),
            "subject_name": subject_request.subject_name,
            "ai_context": subject_doc["ai_context"]
        }
        
    except Exception as e:
        logging.error(f"Error setting up subject: {e}")
        raise HTTPException(status_code=500, detail="Failed to set up subject")

@router.get("/list")
async def list_subjects(user_id: str = None):
    """
    Get list of all subjects for a user
    """
    try:
        subjects_collection = get_subjects_collection()
        
        query = {}
        if user_id:
            query["user_id"] = user_id
            
        subjects = await subjects_collection.find(query).to_list(100)
        
        # Convert ObjectId to string
        for subject in subjects:
            subject["_id"] = str(subject["_id"])
            
        return {"subjects": subjects}
        
    except Exception as e:
        logging.error(f"Error listing subjects: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve subjects")

@router.get("/{subject_id}")
async def get_subject(subject_id: str):
    """
    Get specific subject details
    """
    try:
        subjects_collection = get_subjects_collection()
        
        from bson import ObjectId
        subject = await subjects_collection.find_one({"_id": ObjectId(subject_id)})
        
        if not subject:
            raise HTTPException(status_code=404, detail="Subject not found")
            
        subject["_id"] = str(subject["_id"])
        return subject
        
    except Exception as e:
        logging.error(f"Error getting subject: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve subject")