"""
Health Check Routes

This module provides health check and status endpoints.
"""

from fastapi import APIRouter, Depends
from typing import Dict, Any
import datetime

from ..dependencies import get_ai_service, get_config
from src.core.ai_service import AIService
from config.settings import AppConfig

router = APIRouter()

@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Basic health check endpoint.
    
    Returns:
        Health status information
    """
    return {
        "status": "healthy",
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

@router.get("/health/detailed")
async def detailed_health_check(
    ai_service: AIService = Depends(get_ai_service),
    config: AppConfig = Depends(get_config)
) -> Dict[str, Any]:
    """
    Detailed health check with service status.
    
    Args:
        ai_service: AI service instance
        config: Application configuration
        
    Returns:
        Detailed health status information
    """
    service_status = ai_service.get_service_status()
    
    health_status = {
        "status": "healthy" if service_status["service_initialized"] else "unhealthy",
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "services": {
            "ai_service": service_status["service_initialized"],
            "groq_connection": service_status["connection_status"],
            "config_loaded": True
        },
        "model_info": service_status.get("model_info"),
        "configuration": {
            "model": config.groq_model,
            "max_tokens_summary": config.max_tokens_summary,
            "max_tokens_academic": config.max_tokens_academic
        }
    }
    
    return health_status

@router.get("/status")
async def get_status(
    ai_service: AIService = Depends(get_ai_service)
) -> Dict[str, Any]:
    """
    Get current service status.
    
    Args:
        ai_service: AI service instance
        
    Returns:
        Service status information
    """
    return ai_service.get_service_status()
