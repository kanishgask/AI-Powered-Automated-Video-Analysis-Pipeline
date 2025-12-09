"""
Video downloader module for handling YouTube, cloud storage, and local files
"""

import os
import shutil
from pathlib import Path
from typing import Optional
import yt_dlp
import config
from .utils import is_valid_url, is_youtube_url, is_cloud_storage_url, clean_filename


def download_video(source: str, output_dir: Optional[Path] = None) -> Optional[str]:
    """
    Download or copy video from various sources
    
    Args:
        source: Local file path, YouTube URL, or cloud storage URL
        output_dir: Directory to save downloaded video (default: temp directory)
        
    Returns:
        Path to video file or None if error
    """
    if output_dir is None:
        output_dir = config.TEMP_DIR
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Check if source is a local file
    if os.path.isfile(source):
        return handle_local_file(source, output_dir)
    
    # Check if source is a URL
    if not is_valid_url(source):
        print(f"Error: Invalid source - {source}")
        return None
    
    # Handle YouTube URLs
    if is_youtube_url(source):
        return download_youtube_video(source, output_dir)
    
    # Handle cloud storage URLs
    if is_cloud_storage_url(source):
        return download_cloud_video(source, output_dir)
    
    # Try generic download
    print(f"Attempting generic download from: {source}")
    return download_generic_video(source, output_dir)


def handle_local_file(file_path: str, output_dir: Path) -> Optional[str]:
    """
    Handle local video file
    
    Args:
        file_path: Path to local video file
        output_dir: Directory to copy file to
        
    Returns:
        Path to copied file or original path
    """
    try:
        file_path = Path(file_path).resolve()
        
        if not file_path.exists():
            print(f"Error: File not found - {file_path}")
            return None
        
        # Check if file is already in output directory
        if file_path.parent == output_dir:
            return str(file_path)
        
        # Copy file to output directory
        filename = clean_filename(file_path.name)
        dest_path = output_dir / filename
        
        print(f"Copying local file: {file_path.name}")
        shutil.copy2(file_path, dest_path)
        print(f"File copied to: {dest_path}")
        
        return str(dest_path)
    except Exception as e:
        print(f"Error handling local file: {e}")
        return None


def download_youtube_video(url: str, output_dir: Path) -> Optional[str]:
    """
    Download video from YouTube using yt-dlp
    
    Args:
        url: YouTube URL
        output_dir: Directory to save video
        
    Returns:
        Path to downloaded video file or None if error
    """
    try:
        print(f"Downloading YouTube video: {url}")
        
        # Configure yt-dlp options
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': str(output_dir / '%(title)s.%(ext)s'),
            'quiet': False,
            'no_warnings': False,
            'extract_flat': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Get video info
            info = ydl.extract_info(url, download=False)
            title = clean_filename(info.get('title', 'video'))
            
            # Download video
            ydl.download([url])
            
            # Find downloaded file
            downloaded_files = list(output_dir.glob(f"{title}.*"))
            if downloaded_files:
                video_path = downloaded_files[0]
                print(f"YouTube video downloaded: {video_path}")
                return str(video_path)
            else:
                # Try to find any new video file
                video_extensions = ['.mp4', '.webm', '.mkv', '.flv']
                for ext in video_extensions:
                    files = list(output_dir.glob(f"*{ext}"))
                    if files:
                        print(f"YouTube video downloaded: {files[0]}")
                        return str(files[0])
                
                print("Error: Could not find downloaded video file")
                return None
                
    except Exception as e:
        print(f"Error downloading YouTube video: {e}")
        print("Make sure the URL is valid and the video is accessible")
        return None


def download_cloud_video(url: str, output_dir: Path) -> Optional[str]:
    """
    Download video from cloud storage (Google Drive, Dropbox, etc.)
    
    Args:
        url: Cloud storage URL
        output_dir: Directory to save video
        
    Returns:
        Path to downloaded video file or None if error
    """
    try:
        print(f"Downloading from cloud storage: {url}")
        
        # Use yt-dlp for cloud storage (it supports many cloud services)
        ydl_opts = {
            'format': 'best',
            'outtmpl': str(output_dir / 'cloud_video.%(ext)s'),
            'quiet': False,
            'no_warnings': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
            # Find downloaded file
            video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.webm']
            for ext in video_extensions:
                files = list(output_dir.glob(f"*{ext}"))
                if files:
                    print(f"Cloud video downloaded: {files[0]}")
                    return str(files[0])
            
            print("Error: Could not find downloaded video file")
            return None
            
    except Exception as e:
        print(f"Error downloading cloud video: {e}")
        print("Note: Some cloud storage links may require authentication")
        return None


def download_generic_video(url: str, output_dir: Path) -> Optional[str]:
    """
    Attempt generic video download
    
    Args:
        url: Generic URL
        output_dir: Directory to save video
        
    Returns:
        Path to downloaded video file or None if error
    """
    try:
        print(f"Attempting generic download: {url}")
        
        # Try using yt-dlp as it supports many sites
        ydl_opts = {
            'format': 'best',
            'outtmpl': str(output_dir / 'downloaded_video.%(ext)s'),
            'quiet': False,
            'no_warnings': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
            # Find downloaded file
            video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.webm', '.flv']
            for ext in video_extensions:
                files = list(output_dir.glob(f"*{ext}"))
                if files:
                    print(f"Video downloaded: {files[0]}")
                    return str(files[0])
            
            print("Error: Could not find downloaded video file")
            return None
            
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None

