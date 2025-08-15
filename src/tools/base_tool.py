"""
Base Tool Class

This module provides the base class for all custom CrewAI tools.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class BaseTool(ABC):
    """
    Abstract base class for all custom CrewAI tools.
    
    This class provides common functionality and interface
    that all tools should implement.
    """
    
    def __init__(self, name: str, description: str):
        """
        Initialize the base tool.
        
        Args:
            name: Tool name
            description: Tool description
        """
        self.name = name
        self.description = description
        logger.info(f"Tool initialized: {name}")
    
    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """
        Execute the tool. Must be implemented by subclasses.
        
        Returns:
            Tool execution result
        """
        pass
    
    def get_tool_info(self) -> Dict[str, Any]:
        """
        Get tool information.
        
        Returns:
            Dictionary with tool details
        """
        return {
            "name": self.name,
            "description": self.description,
            "type": self.__class__.__name__
        }
