"""
Academic Service

This module provides specialized services for academic question answering.
"""

from typing import Dict, Any, List
from .crew_service import CrewService
import logging

logger = logging.getLogger(__name__)

class AcademicService:
    """
    Service for academic question answering operations.
    """
    
    def __init__(self, crew_service: CrewService):
        """
        Initialize Academic service.
        
        Args:
            crew_service: CrewService instance
        """
        self.crew_service = crew_service
        logger.info("AcademicService initialized")
    
    def answer_question(self, question: str, subject_area: str = "General") -> Dict[str, Any]:
        """
        Answer an academic question.
        
        Args:
            question: Academic question to answer
            subject_area: Subject area of the question
            
        Returns:
            Dictionary with answer results
        """
        try:
            # Validate input
            if not question.strip():
                return {
                    "success": False,
                    "error": "Question cannot be empty"
                }
            
            # Detect subject area if not provided
            if subject_area == "General":
                subject_area = self._detect_subject_area(question)
            
            # Create and run crew
            crew = self.crew_service.create_academic_crew(
                question=question,
                subject_area=subject_area
            )
            
            result = crew.kickoff()
            
            return {
                "success": True,
                "question": question,
                "subject_area": subject_area,
                "answer": str(result),
                "question_length": len(question),
                "answer_length": len(str(result))
            }
            
        except Exception as e:
            logger.error(f"Academic question answering failed: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _detect_subject_area(self, question: str) -> str:
        """
        Detect the likely subject area of a question.
        
        Args:
            question: Academic question
            
        Returns:
            Detected subject area
        """
        question_lower = question.lower()
        
        # Subject keywords mapping
        subject_keywords = {
            "Mathematics": ["math", "equation", "calculate", "formula", "algebra", "geometry", "calculus"],
            "Physics": ["physics", "force", "energy", "quantum", "mechanics", "thermodynamics"],
            "Chemistry": ["chemistry", "chemical", "reaction", "molecule", "atom", "compound"],
            "Biology": ["biology", "cell", "organism", "evolution", "genetics", "photosynthesis"],
            "Computer Science": ["programming", "algorithm", "code", "software", "computer", "data structure"],
            "History": ["history", "historical", "war", "civilization", "empire", "century"],
            "Literature": ["literature", "poem", "novel", "author", "literary", "shakespeare"],
            "Psychology": ["psychology", "behavior", "mind", "cognitive", "mental", "therapy"],
            "Economics": ["economics", "market", "price", "supply", "demand", "inflation"],
            "Philosophy": ["philosophy", "ethics", "moral", "existence", "logic", "metaphysics"]
        }
        
        # Check for keyword matches
        for subject, keywords in subject_keywords.items():
            if any(keyword in question_lower for keyword in keywords):
                return subject
        
        return "General"
    
    def get_supported_subjects(self) -> List[str]:
        """
        Get list of supported academic subjects.
        
        Returns:
            List of supported subject areas
        """
        return [
            "Mathematics",
            "Physics", 
            "Chemistry",
            "Biology",
            "Computer Science",
            "History",
            "Literature",
            "Psychology",
            "Economics",
            "Philosophy",
            "Geography",
            "Political Science",
            "Sociology",
            "Anthropology",
            "General"
        ]
