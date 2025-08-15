"""
YouTube Tasks

This module contains tasks related to YouTube content analysis.
"""

from .base_task import BaseTask
import logging

logger = logging.getLogger(__name__)

class YouTubeSummaryTask(BaseTask):
    """
    Task for summarizing YouTube video content.
    """
    
    def get_description(self) -> str:
        """Get the task description."""
        return (
            "Analyze the following YouTube video content and create a comprehensive summary:\n\n"
            "Video URL: {video_url}\n"
            "Video ID: {video_id}\n"
            "Content: {content}\n\n"
            "Your analysis should include:\n"
            "1. A brief overview (2-3 sentences)\n"
            "2. Key points and main topics covered\n"
            "3. Important insights or takeaways\n"
            "4. Target audience and relevance\n"
            "5. Educational or practical value\n\n"
            "Make your summary clear, engaging, and informative."
        )
    
    def get_expected_output(self) -> str:
        """Get the expected output description."""
        return (
            "A well-structured summary with:\n"
            "- Brief overview section\n"
            "- Bullet points of key topics\n"
            "- Main insights and takeaways\n"
            "- Target audience analysis\n"
            "- Educational value assessment\n"
            "The summary should be comprehensive yet concise, "
            "helping viewers understand the core value of the content."
        )
