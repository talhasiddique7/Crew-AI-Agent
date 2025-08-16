"""
Academic Service for handling academic questions and chat
"""

import logging
from typing import Dict, Any, List
from ..agents.academic_agent import AcademicAgent

logger = logging.getLogger(__name__)

class AcademicService:
    """Service for academic chat and question answering"""
    
    def __init__(self):
        """Initialize the academic service"""
        self.agent = AcademicAgent()
        logger.info("Academic Service initialized")
    
    def chat(self, message: str, subject: str = "General") -> Dict[str, Any]:
        """
        Handle academic chat messages
        
        Args:
            message: User's message/question
            subject: Subject area
            
        Returns:
            Response dictionary
        """
        try:
            logger.info(f"Processing chat request - Subject: {subject}, Message: {message[:100]}...")
            
            # Use the academic agent to answer the question
            result = self.agent.answer_question(message, subject)
            
            logger.info(f"Agent response - Success: {result['success']}")
            
            if result["success"]:
                return {
                    "success": True,
                    "message": result["answer"],
                    "metadata": {
                        "subject": subject,
                        "agent": "Academic Assistant",
                        "timestamp": self._get_timestamp()
                    }
                }
            else:
                logger.error(f"Agent error: {result.get('error', 'Unknown error')}")
                return {
                    "success": False,
                    "message": "I apologize, but I encountered an error processing your question. Please try again.",
                    "error": result.get("error", "Unknown error")
                }
                
        except Exception as e:
            logger.error(f"Error in academic chat: {e}")
            return {
                "success": False,
                "message": "I'm experiencing technical difficulties. Please try again later.",
                "error": str(e)
            }
    
    def get_subjects(self) -> List[str]:
        """Get list of supported academic subjects"""
        return [
            "General",
            "Mathematics",
            "Physics",
            "Chemistry",
            "Biology",
            "Computer Science",
            "History",
            "Literature",
            "Philosophy",
            "Psychology",
            "Economics",
            "Geography",
            "Political Science",
            "Sociology",
            "Anthropology",
            "Environmental Science",
            "Engineering",
            "Medicine",
            "Law",
            "Education"
        ]
    
    def health_check(self) -> Dict[str, Any]:
        """Check service health"""
        try:
            # Test the LLM connection
            test_result = self.agent.llm.test_connection()
            
            return {
                "service": "Academic Service",
                "status": "healthy" if test_result["success"] else "unhealthy",
                "llm_connection": test_result,
                "agent_status": "initialized"
            }
            
        except Exception as e:
            return {
                "service": "Academic Service",
                "status": "unhealthy",
                "error": str(e)
            }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.utcnow().isoformat() + "Z"
