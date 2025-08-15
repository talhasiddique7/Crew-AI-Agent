"""
YouTube API Routes

This module provides YouTube video analysis endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, HttpUrl, validator
from typing import Dict, Any, Optional
import validators

from ..dependencies import get_ai_service
from src.core.ai_service import AIService
from src.models.request_models import YouTubeRequest, TextAnalysisRequest
from src.models.response_models import YouTubeResponse, TextAnalysisResponse

router = APIRouter()

class YouTubeAnalysisRequest(BaseModel):
    """Request model for YouTube video analysis."""
    video_url: HttpUrl
    
    @validator('video_url')
    def validate_youtube_url(cls, v):
        url_str = str(v)
        if not ('youtube.com' in url_str or 'youtu.be' in url_str):
            raise ValueError('Must be a valid YouTube URL')
        return v

class TextAnalysisAPIRequest(BaseModel):
    """Request model for text analysis."""
    content: str
    title: Optional[str] = "Custom Content"
    
    @validator('content')
    def validate_content(cls, v):
        if not v or not v.strip():
            raise ValueError('Content cannot be empty')
        return v.strip()

class YouTubeAnalysisResponse(BaseModel):
    """Response model for YouTube analysis."""
    success: bool
    video_id: Optional[str] = None
    video_url: Optional[str] = None
    summary: Optional[str] = None
    transcript_length: Optional[int] = None
    error: Optional[str] = None

class TextAnalysisAPIResponse(BaseModel):
    """Response model for text analysis."""
    success: bool
    title: Optional[str] = None
    summary: Optional[str] = None
    content_length: Optional[int] = None
    error: Optional[str] = None

@router.post("/youtube/analyze", response_model=YouTubeAnalysisResponse)
async def analyze_youtube_video(
    request: YouTubeAnalysisRequest,
    ai_service: AIService = Depends(get_ai_service)
) -> YouTubeAnalysisResponse:
    """
    Analyze a YouTube video and generate summary.
    
    Args:
        request: YouTube analysis request
        ai_service: AI service instance
        
    Returns:
        Analysis results
        
    Raises:
        HTTPException: If analysis fails
    """
    try:
        # Convert to internal request model
        youtube_req = YouTubeRequest(video_url=str(request.video_url))
        
        # Perform analysis
        result = ai_service.summarize_youtube_video(str(request.video_url))
        
        # Convert to response model
        return YouTubeAnalysisResponse(
            success=result["success"],
            video_id=result.get("video_id"),
            video_url=result.get("video_url"),
            summary=result.get("summary"),
            transcript_length=result.get("transcript_length"),
            error=result.get("error")
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )

@router.post("/youtube/analyze-text", response_model=TextAnalysisAPIResponse)
async def analyze_text_content(
    request: TextAnalysisAPIRequest,
    ai_service: AIService = Depends(get_ai_service)
) -> TextAnalysisAPIResponse:
    """
    Analyze custom text content.
    
    Args:
        request: Text analysis request
        ai_service: AI service instance
        
    Returns:
        Analysis results
        
    Raises:
        HTTPException: If analysis fails
    """
    try:
        # Convert to internal request model
        text_req = TextAnalysisRequest(
            content=request.content,
            title=request.title
        )
        
        # Perform analysis
        result = ai_service.summarize_text(request.content)
        
        # Convert to response model
        return TextAnalysisAPIResponse(
            success=result["success"],
            title=request.title,
            summary=result.get("summary"),
            content_length=result.get("original_length"),
            error=result.get("error")
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Text analysis failed: {str(e)}"
        )

@router.get("/youtube/video-info/{video_id}")
async def get_video_info(video_id: str) -> Dict[str, Any]:
    """
    Get YouTube video information by ID.
    
    Args:
        video_id: YouTube video ID
        
    Returns:
        Video information
    """
    # Placeholder for video info retrieval
    # In a real implementation, this would fetch metadata from YouTube API
    return {
        "video_id": video_id,
        "title": f"Video {video_id}",
        "description": "Video description placeholder",
        "duration": "Unknown",
        "view_count": "Unknown",
        "upload_date": "Unknown"
    }
