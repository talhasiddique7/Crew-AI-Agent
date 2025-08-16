"""
Simple Academic API routes without CrewAI dependencies
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging
from ..services.simple_academic_service import SimpleAcademicService

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Initialize service
academic_service = SimpleAcademicService()

# Request/Response models
class AcademicQuestionRequest(BaseModel):
    question: str
    subject: str = "General"

class AcademicResponse(BaseModel):
    message: str
    subject: str

@router.post("/chat", response_model=AcademicResponse)
async def academic_chat(request: AcademicQuestionRequest):
    """
    Process academic question and return AI response.
    """
    try:
        logger.info(f"Processing academic question: {request.question[:50]}...")
        
        # Process the question
        response = await academic_service.process_question(
            question=request.question,
            subject=request.subject
        )
        
        logger.info("Academic question processed successfully")
        
        return AcademicResponse(
            message=response,
            subject=request.subject
        )
        
    except Exception as e:
        logger.error(f"Error processing academic question: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing question: {str(e)}"
        )

@router.get("/subjects")
async def get_subjects():
    """
    Get available academic subjects.
    """
    subjects = [
        "General",
        "Mathematics", 
        "Physics",
        "Chemistry",
        "Biology",
        "Computer Science",
        "History",
        "Literature",
        "Economics",
        "Philosophy",
        "Psychology",
        "Engineering",
        "Medicine",
        "Law"
    ]
    
    return {"subjects": subjects}
