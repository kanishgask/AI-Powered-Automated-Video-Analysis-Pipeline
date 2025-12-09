"""
Utility functions for the Meeting Video Captioning & Documentation Program
"""

import os
import shutil
from pathlib import Path
from typing import Optional, Tuple
import re


def format_timestamp(seconds: float) -> str:
    """
    Convert seconds to SRT timestamp format (HH:MM:SS,mmm)
    
    Args:
        seconds: Time in seconds
        
    Returns:
        Formatted timestamp string
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def format_timestamp_readable(seconds: float) -> str:
    """
    Convert seconds to readable format (HH:MM:SS)
    
    Args:
        seconds: Time in seconds
        
    Returns:
        Formatted timestamp string
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def clean_filename(filename: str) -> str:
    """
    Clean filename to remove invalid characters
    
    Args:
        filename: Original filename
        
    Returns:
        Cleaned filename
    """
    # Remove invalid characters for Windows/Linux/Mac
    invalid_chars = r'[<>:"/\\|?*]'
    cleaned = re.sub(invalid_chars, '_', filename)
    # Remove leading/trailing spaces and dots
    cleaned = cleaned.strip(' .')
    return cleaned


def get_video_duration(video_path: str) -> Optional[float]:
    """
    Get video duration in seconds using OpenCV
    
    Args:
        video_path: Path to video file
        
    Returns:
        Duration in seconds or None if error
    """
    try:
        import cv2
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return None
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        duration = frame_count / fps if fps > 0 else None
        
        cap.release()
        return duration
    except Exception as e:
        print(f"Error getting video duration: {e}")
        return None


def ensure_dir(directory: Path) -> Path:
    """
    Ensure directory exists, create if it doesn't
    
    Args:
        directory: Path to directory
        
    Returns:
        Path object
    """
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def is_valid_url(url: str) -> bool:
    """
    Check if string is a valid URL
    
    Args:
        url: String to check
        
    Returns:
        True if valid URL, False otherwise
    """
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url) is not None


def is_youtube_url(url: str) -> bool:
    """
    Check if URL is a YouTube URL
    
    Args:
        url: URL to check
        
    Returns:
        True if YouTube URL, False otherwise
    """
    youtube_patterns = [
        r'youtube\.com',
        r'youtu\.be',
        r'youtube-nocookie\.com'
    ]
    return any(re.search(pattern, url, re.IGNORECASE) for pattern in youtube_patterns)


def is_cloud_storage_url(url: str) -> bool:
    """
    Check if URL is a cloud storage link (Google Drive, Dropbox, etc.)
    
    Args:
        url: URL to check
        
    Returns:
        True if cloud storage URL, False otherwise
    """
    cloud_patterns = [
        r'drive\.google\.com',
        r'dropbox\.com',
        r'onedrive\.live\.com',
        r'1drv\.ms'
    ]
    return any(re.search(pattern, url, re.IGNORECASE) for pattern in cloud_patterns)


def get_file_size_mb(file_path: str) -> float:
    """
    Get file size in megabytes
    
    Args:
        file_path: Path to file
        
    Returns:
        Size in MB
    """
    try:
        size_bytes = os.path.getsize(file_path)
        return size_bytes / (1024 * 1024)
    except Exception:
        return 0.0

