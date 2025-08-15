"""
Academic Agent

This module contains the academic question answering agent.
"""

from crewai import Agent
from .base_agent import BaseAgent
import logging

logger = logging.getLogger(__name__)

class AcademicAgent(BaseAgent):
    """
    Agent specialized in answering academic questions across multiple disciplines.
    """
    
    def _initialize_agent(self) -> None:
        """Initialize the Academic agent."""
        self.agent = Agent(
            role=self.get_role(),
            goal=self.get_goal(),
            backstory=self.get_backstory(),
            llm=self.llm,
            verbose=self.verbose,
            allow_delegation=False
        )
        logger.info("Academic Agent initialized")
    
    def get_role(self) -> str:
        """Get the agent's role description."""
        return "Academic Research Assistant"
    
    def get_goal(self) -> str:
        """Get the agent's goal description."""
        return (
            "Provide comprehensive, accurate, and educational answers to "
            "academic questions across multiple disciplines, helping students "
            "and researchers understand complex concepts with clear explanations "
            "and relevant examples."
        )
    
    def get_backstory(self) -> str:
        """Get the agent's backstory."""
        return (
            "You are a distinguished academic researcher and educator with "
            "expertise spanning multiple disciplines including science, "
            "mathematics, literature, history, philosophy, and social sciences. "
            "You have years of experience in teaching and research, with a "
            "talent for breaking down complex concepts into understandable "
            "explanations. You always provide context, examples, and encourage "
            "critical thinking while maintaining academic rigor and accuracy "
            "in your responses."
        )
