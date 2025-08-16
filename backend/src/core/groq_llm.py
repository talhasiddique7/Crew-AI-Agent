"""
Groq LLM integration for CrewAI
"""

import logging
from typing import Dict, Any, Optional
from groq import Groq
from ..config import config

logger = logging.getLogger(__name__)

class GroqLLM:
    """Groq LLM wrapper for CrewAI integration"""
    
    def __init__(self):
        """Initialize Groq client"""
        self.client = Groq(api_key=config.GROQ_API_KEY)
        self.model = config.GROQ_MODEL
        logger.info(f"Initialized GroqLLM with model: {self.model}")
    
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate response using Groq
        
        Args:
            prompt: Input prompt
            **kwargs: Additional parameters
            
        Returns:
            Generated response
        """
        try:
            logger.info(f"Generating response with Groq - Prompt length: {len(prompt)}")
            
            max_tokens = kwargs.get('max_tokens', config.MAX_TOKENS)
            temperature = kwargs.get('temperature', config.TEMPERATURE)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise e
    
    def test_connection(self) -> Dict[str, Any]:
        """Test connection to Groq API"""
        try:
            response = self.generate("Hello", max_tokens=10)
            return {
                "success": True,
                "message": "Connection successful",
                "response": response[:50] + "..." if len(response) > 50 else response
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Connection failed: {str(e)}"
            }
