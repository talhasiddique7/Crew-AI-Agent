"""
AI service for handling YouTube summarization and academic questions.
"""

import logging
from typing import Dict, Any, Optional
from .groq_llm import GroqLLM
from ..utils.youtube_utils import extract_youtube_id
from config.settings import AppConfig

logger = logging.getLogger(__name__)

class AIService:
    """Main AI service for processing requests."""
    
    def __init__(self, config: AppConfig):
        """
        Initialize AI service.
        
        Args:
            config: Application configuration
        """
        self.config = config
        self.groq_client = None
        
        if config.groq_api_key:
            self.groq_client = GroqLLM(
                api_key=config.groq_api_key,
                model_name=config.groq_model
            )
            logger.info("AI service initialized successfully")
        else:
            logger.warning("No API key provided - AI service not initialized")
    
    def test_connection(self) -> bool:
        """Test AI service connection."""
        if not self.groq_client:
            return False
        return self.groq_client.test_connection()
    
    def summarize_youtube_video(self, url: str) -> Dict[str, Any]:
        """
        Summarize YouTube video from URL.
        
        Args:
            url: YouTube video URL
            
        Returns:
            Dictionary with summary results
        """
        if not self.groq_client:
            return {
                "success": False,
                "error": "AI service not initialized"
            }
        
        try:
            # Extract video ID
            video_id = extract_youtube_id(url)
            if not video_id:
                return {
                    "success": False,
                    "error": "Invalid YouTube URL format"
                }
            
            # For now, return placeholder content since transcript API has issues
            placeholder_content = f"""
            This is a YouTube video analysis for video ID: {video_id}
            
            Note: Due to YouTube transcript API limitations, this is a placeholder analysis.
            For full functionality, please manually paste the video transcript in the manual analysis section.
            """
            
            # Generate summary
            summary = self._generate_summary(placeholder_content)
            
            return {
                "success": True,
                "video_id": video_id,
                "summary": summary,
                "transcript": placeholder_content,
                "transcript_length": len(placeholder_content)
            }
            
        except Exception as e:
            logger.error(f"Error summarizing video: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def summarize_text(self, text: str) -> Dict[str, Any]:
        """
        Summarize provided text content.
        
        Args:
            text: Text content to summarize
            
        Returns:
            Dictionary with summary results
        """
        if not self.groq_client:
            return {
                "success": False,
                "error": "AI service not initialized"
            }
        
        try:
            summary = self._generate_summary(text)
            
            return {
                "success": True,
                "summary": summary,
                "original_length": len(text),
                "summary_length": len(summary)
            }
            
        except Exception as e:
            logger.error(f"Error summarizing text: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def answer_academic_question(self, question: str) -> Dict[str, Any]:
        """
        Answer academic question.
        
        Args:
            question: Academic question to answer
            
        Returns:
            Dictionary with answer results
        """
        if not self.groq_client:
            return {
                "success": False,
                "error": "AI service not initialized"
            }
        
        try:
            prompt = f"""
            Please answer the following academic question comprehensively:
            
            Question: {question}
            
            Please provide:
            1. A clear and direct answer
            2. Explanation of key concepts involved
            3. Examples or applications if relevant
            4. Additional context or related information that might be helpful
            
            Make sure your answer is educational and easy to understand.
            """
            
            answer = self.groq_client.generate(
                prompt=prompt,
                max_tokens=self.config.max_tokens_academic,
                temperature=self.config.temperature
            )
            
            return {
                "success": True,
                "answer": answer,
                "question_length": len(question),
                "answer_length": len(answer)
            }
            
        except Exception as e:
            logger.error(f"Error answering question: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _generate_summary(self, content: str) -> str:
        """
        Generate summary for given content.
        
        Args:
            content: Content to summarize
            
        Returns:
            Generated summary
        """
        prompt = f"""
        Please analyze and summarize the following content:
        
        {content}
        
        Provide:
        1. A brief overview (2-3 sentences)
        2. Key points (3-5 main points)
        3. Important insights or takeaways
        4. Target audience or relevance
        
        Make the summary clear, engaging, and informative.
        """
        
        return self.groq_client.generate(
            prompt=prompt,
            max_tokens=self.config.max_tokens_summary,
            temperature=self.config.temperature
        )
    
    def get_service_status(self) -> Dict[str, Any]:
        """
        Get service status information.
        
        Returns:
            Dictionary with service status
        """
        status = {
            "service_initialized": self.groq_client is not None,
            "connection_status": False,
            "model_info": None
        }
        
        if self.groq_client:
            status["connection_status"] = self.groq_client.test_connection()
            status["model_info"] = self.groq_client.get_model_info()
        
        return status
