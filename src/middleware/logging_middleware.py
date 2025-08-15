"""
Logging Middleware

This module provides logging middleware for request/response tracking.
"""

import logging
import time
from typing import Callable, Any
from functools import wraps

logger = logging.getLogger(__name__)

class LoggingMiddleware:
    """
    Middleware for logging requests and responses.
    """
    
    def __init__(self, log_level: int = logging.INFO):
        """
        Initialize logging middleware.
        
        Args:
            log_level: Logging level
        """
        self.log_level = log_level
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(log_level)
    
    def log_request(self, operation: str, **kwargs):
        """
        Log incoming request.
        
        Args:
            operation: Operation name
            **kwargs: Request parameters
        """
        self.logger.info(f"Request started: {operation}")
        self.logger.debug(f"Request parameters: {kwargs}")
    
    def log_response(self, operation: str, success: bool, duration: float, **kwargs):
        """
        Log response.
        
        Args:
            operation: Operation name
            success: Whether operation was successful
            duration: Operation duration in seconds
            **kwargs: Additional response data
        """
        status = "SUCCESS" if success else "FAILED"
        self.logger.info(f"Request completed: {operation} - {status} - {duration:.2f}s")
        
        if not success and "error" in kwargs:
            self.logger.error(f"Error in {operation}: {kwargs['error']}")
    
    def middleware(self, operation_name: str):
        """
        Decorator for adding logging to functions.
        
        Args:
            operation_name: Name of the operation
            
        Returns:
            Decorator function
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                start_time = time.time()
                
                # Log request
                self.log_request(operation_name, **kwargs)
                
                try:
                    # Execute function
                    result = func(*args, **kwargs)
                    duration = time.time() - start_time
                    
                    # Determine success based on result
                    success = True
                    if hasattr(result, 'success'):
                        success = result.success
                    elif isinstance(result, dict) and 'success' in result:
                        success = result['success']
                    
                    # Log response
                    self.log_response(operation_name, success, duration)
                    
                    return result
                    
                except Exception as e:
                    duration = time.time() - start_time
                    self.log_response(operation_name, False, duration, error=str(e))
                    raise
            
            return wrapper
        return decorator
