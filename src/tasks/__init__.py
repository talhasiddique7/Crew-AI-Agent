"""
CrewAI Tasks Package

This package contains all task definitions for the CrewAI application.
Tasks define the specific work that agents need to accomplish.
"""

from .base_task import BaseTask
from .youtube_tasks import YouTubeSummaryTask
from .academic_tasks import AcademicQuestionTask

__all__ = [
    "BaseTask",
    "YouTubeSummaryTask",
    "AcademicQuestionTask"
]
