"""
CrewAI Agents Package

This package contains all agent definitions for the CrewAI application.
Agents are autonomous entities that can perform specific tasks.
"""

from .base_agent import BaseAgent
from .youtube_agent import YouTubeAgent
from .academic_agent import AcademicAgent

__all__ = [
    "BaseAgent",
    "YouTubeAgent", 
    "AcademicAgent"
]
