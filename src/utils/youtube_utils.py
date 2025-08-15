"""
YouTube utility functions for the CrewAI YouTube agent.
"""

import re
from typing import Optional


def extract_youtube_id(url: str) -> Optional[str]:
    """
    Extract YouTube video ID from various YouTube URL formats.
    
    Args:
        url (str): YouTube URL in various formats
        
    Returns:
        Optional[str]: YouTube video ID if found, None otherwise
        
    Examples:
        >>> extract_youtube_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        "dQw4w9WgXcQ"
        >>> extract_youtube_id("https://youtu.be/dQw4w9WgXcQ")
        "dQw4w9WgXcQ"
        >>> extract_youtube_id("https://www.youtube.com/embed/dQw4w9WgXcQ")
        "dQw4w9WgXcQ"
    """
    # YouTube URL patterns
    patterns = [
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})',
        r'(?:https?://)?(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]{11})',
        r'(?:https?://)?(?:www\.)?youtube\.com/v/([a-zA-Z0-9_-]{11})',
        r'(?:https?://)?youtu\.be/([a-zA-Z0-9_-]{11})',
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?.*v=([a-zA-Z0-9_-]{11})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None


def is_valid_youtube_url(url: str) -> bool:
    """
    Check if a URL is a valid YouTube URL.
    
    Args:
        url (str): URL to validate
        
    Returns:
        bool: True if valid YouTube URL, False otherwise
    """
    return extract_youtube_id(url) is not None


def format_youtube_url(video_id: str) -> str:
    """
    Format a YouTube video ID into a standard YouTube URL.
    
    Args:
        video_id (str): YouTube video ID
        
    Returns:
        str: Formatted YouTube URL
    """
    return f"https://www.youtube.com/watch?v={video_id}"


def get_video_title_from_url(url: str) -> str:
    """
    Extract a readable title from YouTube URL for display purposes.
    
    Args:
        url (str): YouTube URL
        
    Returns:
        str: Formatted title or the video ID
    """
    video_id = extract_youtube_id(url)
    if video_id:
        return f"YouTube Video ({video_id})"
    return "YouTube Video"


def validate_youtube_url(url: str) -> tuple[bool, str]:
    """
    Validate YouTube URL and return validation result with message.
    
    Args:
        url (str): URL to validate
        
    Returns:
        tuple[bool, str]: (is_valid, message)
    """
    if not url or not isinstance(url, str):
        return False, "Please provide a valid URL"
    
    url = url.strip()
    if not url:
        return False, "URL cannot be empty"
    
    if not is_valid_youtube_url(url):
        return False, "Please provide a valid YouTube URL"
    
    return True, "Valid YouTube URL"
