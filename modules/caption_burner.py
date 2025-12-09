"""
Caption burner module for burning SRT subtitles into video using FFmpeg
"""

import os
import subprocess
from pathlib import Path
from typing import Optional
import config
from .utils import ensure_dir


def burn_captions(
    video_path: str,
    srt_path: str,
    output_path: Optional[str] = None
) -> Optional[str]:
    """
    Burn SRT captions into video using FFmpeg
    
    Args:
        video_path: Path to input video file
        srt_path: Path to SRT subtitle file
        output_path: Optional output path for final video
        
    Returns:
        Path to final video with burned captions or None if error
    """
    try:
        video_path = Path(video_path).resolve()
        srt_path = Path(srt_path).resolve()
        
        if not video_path.exists():
            print(f"Error: Video file not found - {video_path}")
            return None
        
        if not srt_path.exists():
            print(f"Error: SRT file not found - {srt_path}")
            return None
        
        # Generate output path if not provided
        if output_path is None:
            ensure_dir(config.FINAL_VIDEOS_DIR)
            output_path = (config.FINAL_VIDEOS_DIR / f"{video_path.stem}_captioned.mp4").resolve()
        else:
            output_path = Path(output_path).resolve()
            output_path.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"Burning captions into video...")
        print(f"Input: {video_path.name}")
        print(f"SRT: {srt_path.name}")
        print(f"Output: {output_path.name}")
        
        # Check if FFmpeg is available
        try:
            subprocess.run(['ffmpeg', '-version'], 
                         capture_output=True, 
                         check=True,
                         timeout=5)
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            print("Error: FFmpeg not found. Please install FFmpeg to burn captions.")
            print("Download from: https://ffmpeg.org/download.html")
            return None
        
        # Build FFmpeg command (absolute paths, forward slashes, quoted SRT)
        video_input = video_path.as_posix()
        srt_input = srt_path.as_posix()
        output_file = output_path.as_posix()

        # Escape filter path for Windows drive colon
        def _escape_filter_path(p: str) -> str:
            return p.replace(":", r"\:").replace("'", r"\'")

        escaped_srt = _escape_filter_path(srt_input)

        force_style = (
            f"FontName=Arial,"
            f"FontSize={config.CAPTION_FONT_SIZE},"
            f"PrimaryColour=&H00FFFFFF&,"  # white
            f"OutlineColour=&H00000000&,"  # black outline
            f"BorderStyle=1,Outline=2,Shadow=0,Alignment=2"
        )
        vf_filter = f"subtitles='{escaped_srt}':force_style='{force_style}'"

        cmd = [
            "ffmpeg",
            "-y",  # Overwrite output file
            "-i", video_input,
            "-sub_charenc", "UTF-8",
            "-vf", vf_filter,
            "-c:v", config.OUTPUT_VIDEO_CODEC,
            "-c:a", "copy",  # keep original audio as requested
            "-preset", "medium",
            "-crf", "23",  # Quality setting (lower = better quality, 18-28 typical range)
            output_file,
        ]
        
        print("Running FFmpeg (this may take a while)...")
        
        # Run FFmpeg
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=3600  # 1 hour timeout
        )
        
        if result.returncode == 0 and output_path.exists():
            file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
            print(f"✓ Captions burned successfully!")
            print(f"  Output: {output_path}")
            print(f"  Size: {file_size_mb:.2f} MB")
            return str(output_path)
        else:
            print("Error: FFmpeg failed to burn captions")
            print(f"Return code: {result.returncode}")
            if result.stdout:
                print(f"FFmpeg stdout:\n{result.stdout[:800]}")
            if result.stderr:
                print(f"FFmpeg stderr:\n{result.stderr[:1200]}")
            return None
            
    except subprocess.TimeoutExpired:
        print("Error: FFmpeg operation timed out (exceeded 1 hour)")
        return None
    except Exception as e:
        print(f"Error burning captions: {e}")
        return None


def create_caption_style_config() -> Optional[str]:
    """
    Create a temporary ASS style file for advanced caption styling
    
    Returns:
        Path to style file or None if error
    """
    try:
        import config
        ensure_dir(config.TEMP_DIR)
        
        style_file = config.TEMP_DIR / "caption_style.ass"
        
        style_content = f"""[Script Info]
Title: Meeting Captions
ScriptType: v4.00+

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,{config.CAPTION_FONT_SIZE},&Hffffff,&Hffffff,&H000000,&H80000000,0,0,0,0,100,100,0,0,1,2,0,2,10,10,10,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        
        with open(style_file, 'w', encoding='utf-8') as f:
            f.write(style_content)
        
        return str(style_file)
        
    except Exception as e:
        print(f"Error creating caption style: {e}")
        return None

