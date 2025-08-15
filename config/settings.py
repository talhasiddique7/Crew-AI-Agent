"""
Application configuration settings.
"""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class AppConfig:
    """Application configuration class."""
    
    # App settings
    app_title: str = "CrewAI AI Assistant"
    app_icon: str = "🤖"
    layout: str = "wide"
    
    # Groq API settings
    groq_api_key: Optional[str] = None
    groq_model: str = "llama3-8b-8192"
    
    # Token limits
    max_tokens_summary: int = 800
    max_tokens_academic: int = 1000
    
    # Temperature settings
    temperature: float = 0.7
    
    def __post_init__(self):
        """Initialize configuration after creation."""
        # Load API key from environment if not provided
        if not self.groq_api_key:
            self.groq_api_key = os.getenv("GROQ_API_KEY")

def get_config() -> AppConfig:
    """Get application configuration."""
    return AppConfig()
