"""
Audio extraction module using FFmpeg or MoviePy
"""

import os
from pathlib import Path
from typing import Optional
import subprocess
import config
from .utils import ensure_dir


def extract_audio(video_path: str, output_path: Optional[str] = None) -> Optional[str]:
    """
    Extract audio from video file
    
    Args:
        video_path: Path to video file
        output_path: Optional output path for audio file
        
    Returns:
        Path to extracted audio file or None if error
    """
    try:
        video_path = Path(video_path)
        
        if not video_path.exists():
            print(f"Error: Video file not found - {video_path}")
            return None
        
        # Generate output path if not provided
        if output_path is None:
            ensure_dir(config.AUDIO_DIR)
            output_path = config.AUDIO_DIR / f"{video_path.stem}.wav"
        else:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"Extracting audio from: {video_path.name}")
        
        # Try FFmpeg first (faster and more reliable)
        if extract_audio_ffmpeg(str(video_path), str(output_path)):
            print(f"Audio extracted: {output_path}")
            return str(output_path)
        
        # Fallback to MoviePy
        print("FFmpeg not available, trying MoviePy...")
        if extract_audio_moviepy(str(video_path), str(output_path)):
            print(f"Audio extracted: {output_path}")
            return str(output_path)
        
        print("Error: Failed to extract audio using both FFmpeg and MoviePy")
        return None
        
    except Exception as e:
        print(f"Error extracting audio: {e}")
        return None


def extract_audio_ffmpeg(video_path: str, output_path: str) -> bool:
    """
    Extract audio using FFmpeg
    
    Args:
        video_path: Path to video file
        output_path: Path to output audio file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Check if FFmpeg is available
        try:
            subprocess.run(['ffmpeg', '-version'], 
                         capture_output=True, 
                         check=True,
                         timeout=5)
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return False
        
        # Extract audio using FFmpeg
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-vn',  # No video
            '-acodec', 'pcm_s16le',  # PCM 16-bit
            '-ar', '16000',  # Sample rate (Whisper works well with 16kHz)
            '-ac', '1',  # Mono
            '-y',  # Overwrite output file
            output_path
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode == 0 and os.path.exists(output_path):
            return True
        else:
            print(f"FFmpeg error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("FFmpeg extraction timed out")
        return False
    except Exception as e:
        print(f"FFmpeg extraction error: {e}")
        return False


def extract_audio_moviepy(video_path: str, output_path: str) -> bool:
    """
    Extract audio using MoviePy
    
    Args:
        video_path: Path to video file
        output_path: Path to output audio file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        from moviepy.editor import VideoFileClip
        
        # Load video
        video = VideoFileClip(video_path)
        
        # Extract audio
        audio = video.audio
        
        if audio is None:
            print("Error: No audio track found in video")
            video.close()
            return False
        
        # Write audio file
        audio.write_audiofile(
            output_path,
            codec='pcm_s16le',
            fps=16000,  # Sample rate for Whisper
            verbose=False,
            logger=None
        )
        
        # Clean up
        audio.close()
        video.close()
        
        return os.path.exists(output_path)
        
    except ImportError:
        print("MoviePy not installed")
        return False
    except Exception as e:
        print(f"MoviePy extraction error: {e}")
        return False

