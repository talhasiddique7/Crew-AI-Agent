"""
Models Package

This package contains data models and schemas used throughout the application.
"""

from .request_models import YouTubeRequest, AcademicRequest
from .response_models import YouTubeResponse, AcademicResponse, ServiceStatus

__all__ = [
    "YouTubeRequest",
    "AcademicRequest", 
    "YouTubeResponse",
    "AcademicResponse",
    "ServiceStatus"
]
