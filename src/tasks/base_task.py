"""
Base Task Class

This module provides the base class for all CrewAI tasks.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from crewai import Task
import logging

logger = logging.getLogger(__name__)

class BaseTask(ABC):
    """
    Abstract base class for all CrewAI tasks.
    
    This class provides common functionality and interface
    that all tasks should implement.
    """
    
    def __init__(self, agent, verbose: bool = True):
        """
        Initialize the base task.
        
        Args:
            agent: CrewAI agent instance
            verbose: Whether to enable verbose logging
        """
        self.agent = agent
        self.verbose = verbose
        self.task = None
    
    @abstractmethod
    def get_description(self) -> str:
        """Get the task description. Must be implemented by subclasses."""
        pass
    
    @abstractmethod
    def get_expected_output(self) -> str:
        """Get the expected output description. Must be implemented by subclasses."""
        pass
    
    def create_task(self, context: Dict[str, Any]) -> Task:
        """
        Create a CrewAI task instance with the given context.
        
        Args:
            context: Context data for the task
            
        Returns:
            CrewAI Task instance
        """
        description = self.get_description().format(**context)
        
        self.task = Task(
            description=description,
            expected_output=self.get_expected_output(),
            agent=self.agent,
            verbose=self.verbose
        )
        
        logger.info(f"Task created: {self.__class__.__name__}")
        return self.task
    
    def get_task_info(self) -> Dict[str, Any]:
        """
        Get task information.
        
        Returns:
            Dictionary with task details
        """
        return {
            "description": self.get_description(),
            "expected_output": self.get_expected_output(),
            "agent_role": self.agent.role if hasattr(self.agent, 'role') else "Unknown",
            "verbose": self.verbose
        }
