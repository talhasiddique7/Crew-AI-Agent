"""
Crew Service

This module provides the main service for orchestrating CrewAI operations.
"""

from typing import Dict, Any, List, Optional
from crewai import Crew, Process
from ..agents import YouTubeAgent, AcademicAgent
from ..tasks import YouTubeSummaryTask, AcademicQuestionTask
from config.settings import AppConfig
import logging

logger = logging.getLogger(__name__)

class CrewService:
    """
    Main service for orchestrating CrewAI agents and tasks.
    """
    
    def __init__(self, config: AppConfig, llm):
        """
        Initialize the crew service.
        
        Args:
            config: Application configuration
            llm: Language model instance
        """
        self.config = config
        self.llm = llm
        self.youtube_agent = None
        self.academic_agent = None
        self._initialize_agents()
        logger.info("CrewService initialized")
    
    def _initialize_agents(self):
        """Initialize all agents."""
        try:
            self.youtube_agent = YouTubeAgent(self.llm)
            self.academic_agent = AcademicAgent(self.llm)
            logger.info("All agents initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize agents: {str(e)}")
            raise
    
    def create_youtube_crew(self, video_url: str, video_id: str, content: str) -> Crew:
        """
        Create a crew for YouTube video analysis.
        
        Args:
            video_url: YouTube video URL
            video_id: YouTube video ID
            content: Video content/transcript
            
        Returns:
            Configured Crew instance
        """
        task = YouTubeSummaryTask(self.youtube_agent.get_agent())
        crew_task = task.create_task({
            "video_url": video_url,
            "video_id": video_id,
            "content": content
        })
        
        crew = Crew(
            agents=[self.youtube_agent.get_agent()],
            tasks=[crew_task],
            process=Process.sequential,
            verbose=True
        )
        
        logger.info(f"YouTube crew created for video: {video_id}")
        return crew
    
    def create_academic_crew(self, question: str, subject_area: str = "General") -> Crew:
        """
        Create a crew for academic question answering.
        
        Args:
            question: Academic question
            subject_area: Subject area of the question
            
        Returns:
            Configured Crew instance
        """
        task = AcademicQuestionTask(self.academic_agent.get_agent())
        crew_task = task.create_task({
            "question": question,
            "subject_area": subject_area
        })
        
        crew = Crew(
            agents=[self.academic_agent.get_agent()],
            tasks=[crew_task],
            process=Process.sequential,
            verbose=True
        )
        
        logger.info(f"Academic crew created for question in {subject_area}")
        return crew
    
    def get_service_status(self) -> Dict[str, Any]:
        """
        Get service status information.
        
        Returns:
            Dictionary with service status
        """
        return {
            "agents_initialized": all([
                self.youtube_agent is not None,
                self.academic_agent is not None
            ]),
            "youtube_agent": self.youtube_agent.get_info() if self.youtube_agent else None,
            "academic_agent": self.academic_agent.get_info() if self.academic_agent else None,
            "llm_model": getattr(self.llm, 'model_name', 'Unknown')
        }
