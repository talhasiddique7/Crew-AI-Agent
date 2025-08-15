"""
Groq LLM integration for CrewAI framework.
"""

import logging
from typing import Optional, Dict, Any
from groq import Groq

logger = logging.getLogger(__name__)

class GroqLLM:
    """Custom LLM wrapper for Groq compatible with CrewAI."""
    
    def __init__(self, api_key: str, model_name: str = "llama3-8b-8192"):
        """
        Initialize Groq LLM.
        
        Args:
            api_key: Groq API key
            model_name: Model name to use
        """
        self.client = Groq(api_key=api_key)
        self.model_name = model_name
        self.api_key = api_key
        logger.info(f"Initialized GroqLLM with model: {model_name}")
    
    def __call__(self, prompt: str, max_tokens: int = 1000, **kwargs) -> str:
        """Make the instance callable."""
        return self.generate(prompt, max_tokens, **kwargs)
    
    def generate(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7) -> str:
        """
        Generate response using Groq.
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            Generated response
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            logger.error(error_msg)
            return error_msg
    
    def test_connection(self) -> bool:
        """
        Test connection to Groq API.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            response = self.generate("Hello", max_tokens=5)
            return not response.startswith("Error")
        except Exception as e:
            logger.error(f"Connection test failed: {str(e)}")
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get model information.
        
        Returns:
            Dictionary with model information
        """
        return {
            "model_name": self.model_name,
            "provider": "Groq",
            "type": "LLM",
            "connection_status": self.test_connection()
        }
