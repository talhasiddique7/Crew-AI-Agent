"""
Academic API Routes

This module provides academic question answering endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, validator
from typing import Dict, Any, Optional, List
from enum import Enum

from ..dependencies import get_ai_service
from src.core.ai_service import AIService
from src.models.request_models import AcademicRequest
from src.models.response_models import AcademicResponse

router = APIRouter()

class SubjectArea(str, Enum):
    """Supported academic subject areas."""
    GENERAL = "General"
    MATHEMATICS = "Mathematics"
    PHYSICS = "Physics"
    CHEMISTRY = "Chemistry"
    BIOLOGY = "Biology"
    COMPUTER_SCIENCE = "Computer Science"
    HISTORY = "History"
    LITERATURE = "Literature"
    PSYCHOLOGY = "Psychology"
    ECONOMICS = "Economics"
    PHILOSOPHY = "Philosophy"
    GEOGRAPHY = "Geography"
    POLITICAL_SCIENCE = "Political Science"
    SOCIOLOGY = "Sociology"
    ANTHROPOLOGY = "Anthropology"

class AcademicQuestionRequest(BaseModel):
    """Request model for academic questions."""
    question: str
    subject_area: Optional[SubjectArea] = SubjectArea.GENERAL
    
    @validator('question')
    def validate_question(cls, v):
        if not v or not v.strip():
            raise ValueError('Question cannot be empty')
        return v.strip()

class AcademicQuestionResponse(BaseModel):
    """Response model for academic answers."""
    success: bool
    question: Optional[str] = None
    subject_area: Optional[str] = None
    answer: Optional[str] = None
    question_length: Optional[int] = None
    answer_length: Optional[int] = None
    error: Optional[str] = None

@router.post("/academic/ask", response_model=AcademicQuestionResponse)
async def ask_academic_question(
    request: AcademicQuestionRequest,
    ai_service: AIService = Depends(get_ai_service)
) -> AcademicQuestionResponse:
    """
    Answer an academic question.
    
    Args:
        request: Academic question request
        ai_service: AI service instance
        
    Returns:
        Academic answer
        
    Raises:
        HTTPException: If answering fails
    """
    try:
        # Convert to internal request model
        academic_req = AcademicRequest(
            question=request.question,
            subject_area=request.subject_area.value
        )
        
        # Get answer
        result = ai_service.answer_academic_question(request.question)
        
        # Convert to response model
        return AcademicQuestionResponse(
            success=result["success"],
            question=result.get("question"),
            subject_area=result.get("subject_area"),
            answer=result.get("answer"),
            question_length=result.get("question_length"),
            answer_length=result.get("answer_length"),
            error=result.get("error")
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to answer question: {str(e)}"
        )

@router.get("/academic/subjects", response_model=List[str])
async def get_supported_subjects() -> List[str]:
    """
    Get list of supported academic subjects.
    
    Returns:
        List of supported subject areas
    """
    return [subject.value for subject in SubjectArea]

@router.get("/academic/subjects/details")
async def get_subject_details() -> Dict[str, Any]:
    """
    Get detailed information about supported subjects.
    
    Returns:
        Detailed subject information
    """
    subject_details = {
        "Mathematics": {
            "description": "Algebra, geometry, calculus, statistics, and mathematical analysis",
            "topics": ["Algebra", "Geometry", "Calculus", "Statistics", "Linear Algebra"]
        },
        "Physics": {
            "description": "Classical mechanics, thermodynamics, electromagnetism, quantum physics",
            "topics": ["Mechanics", "Thermodynamics", "Electromagnetism", "Quantum Physics"]
        },
        "Chemistry": {
            "description": "Organic, inorganic, physical chemistry, and biochemistry",
            "topics": ["Organic Chemistry", "Inorganic Chemistry", "Physical Chemistry", "Biochemistry"]
        },
        "Biology": {
            "description": "Cell biology, genetics, evolution, ecology, and physiology",
            "topics": ["Cell Biology", "Genetics", "Evolution", "Ecology", "Physiology"]
        },
        "Computer Science": {
            "description": "Programming, algorithms, data structures, and software engineering",
            "topics": ["Programming", "Algorithms", "Data Structures", "Software Engineering"]
        },
        "History": {
            "description": "World history, civilizations, historical analysis, and historiography",
            "topics": ["Ancient History", "Medieval History", "Modern History", "World Wars"]
        },
        "Literature": {
            "description": "Literary analysis, poetry, prose, drama, and literary criticism",
            "topics": ["Poetry", "Prose", "Drama", "Literary Criticism", "World Literature"]
        },
        "Psychology": {
            "description": "Cognitive psychology, behavioral psychology, and psychological research",
            "topics": ["Cognitive Psychology", "Behavioral Psychology", "Developmental Psychology"]
        },
        "Economics": {
            "description": "Microeconomics, macroeconomics, economic theory, and market analysis",
            "topics": ["Microeconomics", "Macroeconomics", "Economic Theory", "Market Analysis"]
        },
        "Philosophy": {
            "description": "Ethics, logic, metaphysics, and philosophical reasoning",
            "topics": ["Ethics", "Logic", "Metaphysics", "Political Philosophy"]
        }
    }
    
    return {
        "total_subjects": len(SubjectArea),
        "subjects": subject_details,
        "general_note": "General category accepts questions from any academic field"
    }

@router.post("/academic/batch-questions")
async def answer_batch_questions(
    questions: List[AcademicQuestionRequest],
    ai_service: AIService = Depends(get_ai_service)
) -> List[AcademicQuestionResponse]:
    """
    Answer multiple academic questions in batch.
    
    Args:
        questions: List of academic questions
        ai_service: AI service instance
        
    Returns:
        List of academic answers
        
    Raises:
        HTTPException: If batch processing fails
    """
    if len(questions) > 10:  # Limit batch size
        raise HTTPException(
            status_code=400,
            detail="Batch size cannot exceed 10 questions"
        )
    
    results = []
    for question_req in questions:
        try:
            result = ai_service.answer_academic_question(question_req.question)
            
            response = AcademicQuestionResponse(
                success=result["success"],
                question=result.get("question"),
                subject_area=result.get("subject_area"),
                answer=result.get("answer"),
                question_length=result.get("question_length"),
                answer_length=result.get("answer_length"),
                error=result.get("error")
            )
            results.append(response)
            
        except Exception as e:
            error_response = AcademicQuestionResponse(
                success=False,
                question=question_req.question,
                error=str(e)
            )
            results.append(error_response)
    
    return results
