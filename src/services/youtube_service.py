"""
YouTube Service

This module provides specialized services for YouTube content processing.
"""

from typing import Dict, Any
from .crew_service import CrewService
from ..utils.youtube_utils import extract_youtube_id, validate_youtube_url
from ..tools.youtube_tools import YouTubeTranscriptTool
import logging

logger = logging.getLogger(__name__)

class YouTubeService:
    """
    Service for YouTube content analysis operations.
    """
    
    def __init__(self, crew_service: CrewService):
        """
        Initialize YouTube service.
        
        Args:
            crew_service: CrewService instance
        """
        self.crew_service = crew_service
        self.transcript_tool = YouTubeTranscriptTool()
        logger.info("YouTubeService initialized")
    
    def analyze_video(self, video_url: str) -> Dict[str, Any]:
        """
        Analyze YouTube video and generate summary.
        
        Args:
            video_url: YouTube video URL
            
        Returns:
            Dictionary with analysis results
        """
        try:
            # Validate URL
            if not validate_youtube_url(video_url):
                return {
                    "success": False,
                    "error": "Invalid YouTube URL format"
                }
            
            # Extract video ID
            video_id = extract_youtube_id(video_url)
            if not video_id:
                return {
                    "success": False,
                    "error": "Could not extract video ID from URL"
                }
            
            # Get transcript
            transcript_result = self.transcript_tool.execute(video_url)
            if not transcript_result["success"]:
                return {
                    "success": False,
                    "error": f"Transcript extraction failed: {transcript_result['error']}"
                }
            
            # Create and run crew
            crew = self.crew_service.create_youtube_crew(
                video_url=video_url,
                video_id=video_id,
                content=transcript_result["transcript"]
            )
            
            result = crew.kickoff()
            
            return {
                "success": True,
                "video_id": video_id,
                "video_url": video_url,
                "summary": str(result),
                "transcript": transcript_result["transcript"],
                "transcript_length": len(transcript_result["transcript"])
            }
            
        except Exception as e:
            logger.error(f"YouTube analysis failed: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def analyze_text_content(self, content: str, title: str = "Custom Content") -> Dict[str, Any]:
        """
        Analyze custom text content as if it were YouTube content.
        
        Args:
            content: Text content to analyze
            title: Title for the content
            
        Returns:
            Dictionary with analysis results
        """
        try:
            # Create crew for content analysis
            crew = self.crew_service.create_youtube_crew(
                video_url="Custom Content",
                video_id=title,
                content=content
            )
            
            result = crew.kickoff()
            
            return {
                "success": True,
                "title": title,
                "summary": str(result),
                "content": content,
                "content_length": len(content)
            }
            
        except Exception as e:
            logger.error(f"Text content analysis failed: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
