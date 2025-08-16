"""
Academic API routes
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import logging

from ..services.academic_service import AcademicService

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize service
academic_service = AcademicService()

class ChatRequest(BaseModel):
    """Request model for academic chat"""
    message: str
    subject: Optional[str] = "General"

class ChatResponse(BaseModel):
    """Response model for academic chat"""
    success: bool
    message: str
    metadata: Optional[dict] = None
    error: Optional[str] = None

@router.post("/chat", response_model=ChatResponse)
async def academic_chat(request: ChatRequest):
    """
    Academic chat endpoint
    
    Send a message to the academic assistant and get a response.
    """
    try:
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        result = academic_service.chat(request.message, request.subject)
        
        return ChatResponse(
            success=result["success"],
            message=result["message"],
            metadata=result.get("metadata"),
            error=result.get("error")
        )
        
    except Exception as e:
        logger.error(f"Error in academic chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/subjects")
async def get_subjects():
    """Get list of supported academic subjects"""
    try:
        subjects = academic_service.get_subjects()
        return {
            "subjects": subjects,
            "total": len(subjects)
        }
    except Exception as e:
        logger.error(f"Error getting subjects: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/health")
async def academic_health():
    """Health check for academic service"""
    try:
        health = academic_service.health_check()
        return health
    except Exception as e:
        logger.error(f"Error in academic health check: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
