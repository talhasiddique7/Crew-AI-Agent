"""
API Dependencies

This module provides dependency injection for FastAPI routes.
"""

from fastapi import Depends, HTTPException, Header
from typing import Optional
import os

from config.settings import get_config, AppConfig
from src.core.ai_service import AIService

# Global instances
_config: Optional[AppConfig] = None
_ai_service: Optional[AIService] = None

def get_config() -> AppConfig:
    """
    Get application configuration.
    
    Returns:
        Application configuration instance
    """
    global _config
    if _config is None:
        _config = get_config()
    return _config

def get_ai_service(config: AppConfig = Depends(get_config)) -> AIService:
    """
    Get AI service instance.
    
    Args:
        config: Application configuration
        
    Returns:
        AI service instance
        
    Raises:
        HTTPException: If service initialization fails
    """
    global _ai_service
    
    if _ai_service is None:
        try:
            _ai_service = AIService(config)
            if not _ai_service.test_connection():
                raise HTTPException(
                    status_code=503,
                    detail="AI service connection failed"
                )
        except Exception as e:
            raise HTTPException(
                status_code=503,
                detail=f"Failed to initialize AI service: {str(e)}"
            )
    
    return _ai_service

def get_api_key(authorization: Optional[str] = Header(None)) -> Optional[str]:
    """
    Extract API key from Authorization header.
    
    Args:
        authorization: Authorization header value
        
    Returns:
        API key if present
    """
    if authorization and authorization.startswith("Bearer "):
        return authorization[7:]
    return None

def validate_api_key(api_key: Optional[str] = Depends(get_api_key)) -> str:
    """
    Validate API key (if authentication is required).
    
    Args:
        api_key: API key from header
        
    Returns:
        Validated API key
        
    Raises:
        HTTPException: If API key is invalid
    """
    # For now, just check if API key is provided
    # In production, implement proper validation
    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="API key required"
        )
    
    return api_key

def get_rate_limit_info(user_id: Optional[str] = None) -> dict:
    """
    Get rate limit information for user.
    
    Args:
        user_id: User identifier
        
    Returns:
        Rate limit information
    """
    # Placeholder for rate limiting logic
    return {
        "requests_remaining": 100,
        "reset_time": "2024-01-01T00:00:00Z"
    }
