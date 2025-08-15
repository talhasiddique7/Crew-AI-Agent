"""
Base Agent Class

This module provides the base class for all CrewAI agents.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from crewai import Agent
import logging

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """
    Abstract base class for all CrewAI agents.
    
    This class provides common functionality and interface
    that all agents should implement.
    """
    
    def __init__(self, llm, verbose: bool = True):
        """
        Initialize the base agent.
        
        Args:
            llm: Language model instance
            verbose: Whether to enable verbose logging
        """
        self.llm = llm
        self.verbose = verbose
        self.agent = None
        self._initialize_agent()
    
    @abstractmethod
    def _initialize_agent(self) -> None:
        """Initialize the CrewAI agent. Must be implemented by subclasses."""
        pass
    
    @abstractmethod
    def get_role(self) -> str:
        """Get the agent's role description."""
        pass
    
    @abstractmethod
    def get_goal(self) -> str:
        """Get the agent's goal description.""" 
        pass
    
    @abstractmethod
    def get_backstory(self) -> str:
        """Get the agent's backstory."""
        pass
    
    def get_agent(self) -> Agent:
        """
        Get the CrewAI agent instance.
        
        Returns:
            CrewAI Agent instance
        """
        return self.agent
    
    def get_info(self) -> Dict[str, Any]:
        """
        Get agent information.
        
        Returns:
            Dictionary with agent details
        """
        return {
            "role": self.get_role(),
            "goal": self.get_goal(),
            "backstory": self.get_backstory(),
            "verbose": self.verbose
        }
