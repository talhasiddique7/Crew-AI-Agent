"""
FastAPI Application Package

This package contains the FastAPI REST API for the CrewAI application.
"""

from .app import create_app
from .dependencies import get_ai_service, get_config

__all__ = [
    "create_app",
    "get_ai_service",
    "get_config"
]
