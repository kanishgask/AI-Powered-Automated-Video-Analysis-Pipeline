"""
Configuration file for Meeting Video Captioning & Documentation Program
"""

import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "outputs"
CAPTIONS_DIR = OUTPUT_DIR / "captions"
FRAMES_DIR = OUTPUT_DIR / "frames"
REPORTS_DIR = OUTPUT_DIR / "reports"
FINAL_VIDEOS_DIR = OUTPUT_DIR / "final_videos"
AUDIO_DIR = OUTPUT_DIR / "audio"
TEMP_DIR = OUTPUT_DIR / "temp"

# Create directories if they don't exist
for directory in [OUTPUT_DIR, CAPTIONS_DIR, FRAMES_DIR, REPORTS_DIR, FINAL_VIDEOS_DIR, AUDIO_DIR, TEMP_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Video settings
SUPPORTED_VIDEO_FORMATS = ['.mp4', '.mov', '.avi', '.mkv', '.webm', '.flv']
SUPPORTED_AUDIO_FORMATS = ['.wav', '.mp3', '.m4a']

# Whisper settings
WHISPER_MODEL = "base"  # Options: tiny, base, small, medium, large
WHISPER_LANGUAGE = None  # None for auto-detection

# Scene detection settings
SCENE_CHANGE_THRESHOLD = 0.3  # SSIM threshold for scene changes (0-1)
FRAME_SAMPLE_RATE = 1  # Process every Nth frame (1 = all frames)
CLICK_DETECTION_THRESHOLD = 0.1  # Frame difference threshold for click detection
MIN_SCENE_DURATION = 2.0  # Minimum seconds between scene changes

# Report settings
REPORT_FORMAT = "docx"  # Options: "docx" or "pdf"
INCLUDE_SCREENSHOTS = True
INCLUDE_TRANSCRIPT = True
INCLUDE_CLICK_LOG = True

# Caption settings
CAPTION_FONT_SIZE = 24
CAPTION_FONT_COLOR = "white"
CAPTION_BACKGROUND_COLOR = "black"
CAPTION_POSITION = "bottom"  # Options: "top", "bottom", "center"

# FFmpeg settings
FFMPEG_QUALITY = "high"  # Options: "low", "medium", "high"
OUTPUT_VIDEO_CODEC = "libx264"
OUTPUT_AUDIO_CODEC = "aac"

