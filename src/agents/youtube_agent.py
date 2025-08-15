"""
YouTube Agent

This module contains the YouTube content analysis agent.
"""

from crewai import Agent
from .base_agent import BaseAgent
import logging

logger = logging.getLogger(__name__)

class YouTubeAgent(BaseAgent):
    """
    Agent specialized in YouTube content analysis and summarization.
    """
    
    def _initialize_agent(self) -> None:
        """Initialize the YouTube agent."""
        self.agent = Agent(
            role=self.get_role(),
            goal=self.get_goal(), 
            backstory=self.get_backstory(),
            llm=self.llm,
            verbose=self.verbose,
            allow_delegation=False
        )
        logger.info("YouTube Agent initialized")
    
    def get_role(self) -> str:
        """Get the agent's role description."""
        return "YouTube Content Analyst"
    
    def get_goal(self) -> str:
        """Get the agent's goal description."""
        return (
            "Analyze YouTube video content and provide comprehensive, "
            "structured summaries that highlight key points, insights, "
            "and educational value for viewers."
        )
    
    def get_backstory(self) -> str:
        """Get the agent's backstory."""
        return (
            "You are an expert content analyst with years of experience "
            "in digital media and educational content. You specialize in "
            "extracting meaningful insights from video content and presenting "
            "them in a clear, structured format that helps viewers understand "
            "the core messages and value of the content. You have a keen eye "
            "for identifying key themes, target audiences, and practical "
            "applications of the information presented."
        )
