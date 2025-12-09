"""
Transcription module using OpenAI Whisper
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import whisper
import config
from .utils import format_timestamp, ensure_dir


def transcribe_audio(audio_path: str, model_name: Optional[str] = None) -> Optional[Dict]:
    """
    Transcribe audio using Whisper
    
    Args:
        audio_path: Path to audio file
        model_name: Whisper model name (default from config)
        
    Returns:
        Dictionary with transcription results or None if error
    """
    try:
        audio_path = Path(audio_path)
        
        if not audio_path.exists():
            print(f"Error: Audio file not found - {audio_path}")
            return None
        
        if model_name is None:
            model_name = config.WHISPER_MODEL
        
        print(f"Loading Whisper model: {model_name}")
        print("Note: First run will download the model (this may take a few minutes)")
        
        # Load Whisper model
        model = whisper.load_model(model_name)
        
        print(f"Transcribing audio: {audio_path.name}")
        print("This may take a while depending on audio length...")
        
        # Transcribe
        result = model.transcribe(
            str(audio_path),
            language=config.WHISPER_LANGUAGE,
            verbose=False
        )
        
        print("Transcription completed!")
        
        return result
        
    except Exception as e:
        print(f"Error during transcription: {e}")
        return None


def generate_srt(transcription_result: Dict, output_path: Optional[str] = None) -> Optional[str]:
    """
    Generate SRT subtitle file from Whisper transcription
    
    Args:
        transcription_result: Whisper transcription result dictionary
        output_path: Optional output path for SRT file
        
    Returns:
        Path to SRT file or None if error
    """
    try:
        if output_path is None:
            ensure_dir(config.CAPTIONS_DIR)
            output_path = config.CAPTIONS_DIR / "captions.srt"
        else:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
        
        segments = transcription_result.get('segments', [])
        
        if not segments:
            print("Error: No segments found in transcription")
            return None
        
        print(f"Generating SRT file: {output_path}")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for i, segment in enumerate(segments, 1):
                start_time = format_timestamp(segment['start'])
                end_time = format_timestamp(segment['end'])
                text = segment['text'].strip()
                
                # Write SRT entry
                f.write(f"{i}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{text}\n\n")
        
        print(f"SRT file generated: {output_path}")
        return str(output_path)
        
    except Exception as e:
        print(f"Error generating SRT: {e}")
        return None


def get_full_transcript(transcription_result: Dict) -> str:
    """
    Get full transcript text from Whisper result
    
    Args:
        transcription_result: Whisper transcription result dictionary
        
    Returns:
        Full transcript text
    """
    return transcription_result.get('text', '').strip()


def get_segments(transcription_result: Dict) -> List[Dict]:
    """
    Get transcription segments with timestamps
    
    Args:
        transcription_result: Whisper transcription result dictionary
        
    Returns:
        List of segment dictionaries
    """
    return transcription_result.get('segments', [])


def save_transcription_json(transcription_result: Dict, output_path: Optional[str] = None) -> Optional[str]:
    """
    Save transcription result as JSON
    
    Args:
        transcription_result: Whisper transcription result dictionary
        output_path: Optional output path for JSON file
        
    Returns:
        Path to JSON file or None if error
    """
    try:
        if output_path is None:
            ensure_dir(config.CAPTIONS_DIR)
            output_path = config.CAPTIONS_DIR / "transcription.json"
        else:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(transcription_result, f, indent=2, ensure_ascii=False)
        
        print(f"Transcription JSON saved: {output_path}")
        return str(output_path)
        
    except Exception as e:
        print(f"Error saving transcription JSON: {e}")
        return None

