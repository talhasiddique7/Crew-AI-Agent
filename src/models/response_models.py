"""
Response Models

This module contains data models for API responses.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any, List

@dataclass
class BaseResponse:
    """Base response model."""
    
    success: bool
    error: Optional[str] = None
    
    @property
    def is_success(self) -> bool:
        """Check if the response indicates success."""
        return self.success and not self.error

@dataclass
class YouTubeResponse(BaseResponse):
    """Model for YouTube analysis responses."""
    
    video_id: Optional[str] = None
    video_url: Optional[str] = None
    summary: Optional[str] = None
    transcript: Optional[str] = None
    transcript_length: Optional[int] = None
    
    @property
    def has_content(self) -> bool:
        """Check if response has content."""
        return bool(self.summary and self.transcript)

@dataclass
class AcademicResponse(BaseResponse):
    """Model for academic question responses."""
    
    question: Optional[str] = None
    subject_area: Optional[str] = None
    answer: Optional[str] = None
    question_length: Optional[int] = None
    answer_length: Optional[int] = None
    
    @property
    def has_answer(self) -> bool:
        """Check if response has an answer."""
        return bool(self.answer)

@dataclass
class TextAnalysisResponse(BaseResponse):
    """Model for text analysis responses."""
    
    title: Optional[str] = None
    summary: Optional[str] = None
    content: Optional[str] = None
    content_length: Optional[int] = None
    
    @property
    def has_summary(self) -> bool:
        """Check if response has a summary."""
        return bool(self.summary)

@dataclass
class ServiceStatus:
    """Model for service status information."""
    
    agents_initialized: bool
    youtube_agent: Optional[Dict[str, Any]] = None
    academic_agent: Optional[Dict[str, Any]] = None
    llm_model: Optional[str] = None
    connection_status: bool = False
    
    @property
    def is_ready(self) -> bool:
        """Check if service is ready."""
        return self.agents_initialized and self.connection_status

@dataclass
class HealthCheck:
    """Model for health check responses."""
    
    status: str  # "healthy", "degraded", "unhealthy"
    timestamp: str
    services: Dict[str, bool]
    version: Optional[str] = None
    
    @property
    def is_healthy(self) -> bool:
        """Check if system is healthy."""
        return self.status == "healthy" and all(self.services.values())
