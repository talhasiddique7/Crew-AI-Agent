"""
Request Models

This module contains data models for API requests.
"""

from dataclasses import dataclass
from typing import Optional
import validators

@dataclass
class YouTubeRequest:
    """Model for YouTube analysis requests."""
    
    video_url: str
    
    def __post_init__(self):
        """Validate the request after initialization."""
        if not self.video_url:
            raise ValueError("Video URL is required")
        
        if not validators.url(self.video_url):
            raise ValueError("Invalid URL format")
    
    @property
    def is_valid(self) -> bool:
        """Check if the request is valid."""
        try:
            return validators.url(self.video_url) and "youtube" in self.video_url.lower()
        except:
            return False

@dataclass
class AcademicRequest:
    """Model for academic question requests."""
    
    question: str
    subject_area: Optional[str] = "General"
    
    def __post_init__(self):
        """Validate the request after initialization."""
        if not self.question or not self.question.strip():
            raise ValueError("Question is required")
        
        self.question = self.question.strip()
    
    @property
    def is_valid(self) -> bool:
        """Check if the request is valid."""
        return bool(self.question and self.question.strip())

@dataclass
class TextAnalysisRequest:
    """Model for custom text analysis requests."""
    
    content: str
    title: Optional[str] = "Custom Content"
    
    def __post_init__(self):
        """Validate the request after initialization."""
        if not self.content or not self.content.strip():
            raise ValueError("Content is required")
        
        self.content = self.content.strip()
        if not self.title:
            self.title = "Custom Content"
    
    @property
    def is_valid(self) -> bool:
        """Check if the request is valid."""
        return bool(self.content and self.content.strip())
