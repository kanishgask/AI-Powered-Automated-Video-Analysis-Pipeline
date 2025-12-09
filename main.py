"""
Meeting Video Captioning & Documentation Program
Main entry point - One-click script to process meeting videos
"""

import sys
from pathlib import Path
import config

# Import modules
from modules.downloader import download_video
from modules.audio_extractor import extract_audio
from modules.transcription import transcribe_audio, generate_srt, get_full_transcript, get_segments
from modules.scene_detection import detect_scenes, detect_clicks
from modules.report_generator import generate_report
from modules.caption_burner import burn_captions
from modules.utils import clean_filename, format_timestamp_readable


def print_banner():
    """Print program banner"""
    print("\n" + "="*70)
    print("  Meeting Video Captioning & Documentation Program")
    print("="*70)
    print()


def print_summary(results: dict):
    """Print processing summary"""
    print("\n" + "="*70)
    print("  PROCESSING COMPLETE!")
    print("="*70)
    print()
    
    if results.get('video_path'):
        print(f"✓ Video processed: {Path(results['video_path']).name}")
    
    if results.get('audio_path'):
        print(f"✓ Audio extracted: {Path(results['audio_path']).name}")
    
    if results.get('transcription_result'):
        segments = get_segments(results['transcription_result'])
        if segments:
            duration = segments[-1].get('end', 0)
            print(f"✓ Transcription completed: {len(segments)} segments, "
                  f"Duration: {format_timestamp_readable(duration)}")
    
    if results.get('srt_path'):
        print(f"✓ SRT captions generated: {Path(results['srt_path']).name}")
    
    if results.get('scene_changes'):
        print(f"✓ Scene detection: {len(results['scene_changes'])} scene changes detected")
    
    if results.get('clicks'):
        print(f"✓ UI interactions: {len(results['clicks'])} interactions detected")
    
    if results.get('report_path'):
        print(f"✓ Report generated: {Path(results['report_path']).name}")
    
    if results.get('final_video_path'):
        print(f"✓ Final video with captions: {Path(results['final_video_path']).name}")
    
    print("\n" + "="*70)
    print("  OUTPUT FILES")
    print("="*70)
    print()
    
    print(f"📁 Output directory: {config.OUTPUT_DIR}")
    print(f"  ├── Captions: {config.CAPTIONS_DIR}")
    print(f"  ├── Frames: {config.FRAMES_DIR}")
    print(f"  ├── Reports: {config.REPORTS_DIR}")
    print(f"  └── Final Videos: {config.FINAL_VIDEOS_DIR}")
    print()
    
    if results.get('srt_path'):
        print(f"📄 SRT File: {results['srt_path']}")
    if results.get('report_path'):
        print(f"📄 Report: {results['report_path']}")
    if results.get('final_video_path'):
        print(f"🎬 Final Video: {results['final_video_path']}")
    print()


def main():
    """Main processing function"""
    print_banner()
    
    # Get input from user
    print("Enter video source:")
    print("  - Local file path (e.g., /path/to/video.mp4)")
    print("  - YouTube URL (e.g., https://www.youtube.com/watch?v=...)")
    print("  - Cloud storage link (Google Drive, Dropbox, etc.)")
    print()
    
    source = input("Source: ").strip()
    
    if not source:
        print("Error: No source provided")
        sys.exit(1)
    
    # Results dictionary
    results = {}
    
    try:
        # Step 1: Download/Load video
        print("\n" + "-"*70)
        print("STEP 1: Downloading/Loading Video")
        print("-"*70)
        video_path = download_video(source)
        
        if not video_path:
            print("Error: Failed to download/load video")
            sys.exit(1)
        
        results['video_path'] = video_path
        print(f"✓ Video ready: {Path(video_path).name}")
        
        # Step 2: Extract audio
        print("\n" + "-"*70)
        print("STEP 2: Extracting Audio")
        print("-"*70)
        audio_path = extract_audio(video_path)
        
        if not audio_path:
            print("Error: Failed to extract audio")
            sys.exit(1)
        
        results['audio_path'] = audio_path
        print(f"✓ Audio extracted: {Path(audio_path).name}")
        
        # Step 3: Transcribe audio
        print("\n" + "-"*70)
        print("STEP 3: Transcribing Audio with Whisper")
        print("-"*70)
        transcription_result = transcribe_audio(audio_path)
        
        if not transcription_result:
            print("Error: Failed to transcribe audio")
            sys.exit(1)
        
        results['transcription_result'] = transcription_result
        
        # Generate SRT file
        srt_path = generate_srt(transcription_result)
        if srt_path:
            results['srt_path'] = srt_path
        
        # Step 4: Detect scenes and clicks
        print("\n" + "-"*70)
        print("STEP 4: Detecting Scene Changes & UI Interactions")
        print("-"*70)
        scene_changes = detect_scenes(video_path)
        results['scene_changes'] = scene_changes
        
        clicks = detect_clicks(video_path, scene_changes)
        results['clicks'] = clicks
        
        # Step 5: Generate report
        print("\n" + "-"*70)
        print("STEP 5: Generating Meeting Report")
        print("-"*70)
        report_path = generate_report(
            video_path,
            transcription_result,
            scene_changes,
            clicks
        )
        
        if report_path:
            results['report_path'] = report_path
        
        # Step 6: Burn captions into video
        print("\n" + "-"*70)
        print("STEP 6: Burning Captions into Video")
        print("-"*70)
        
        if srt_path:
            final_video_path = burn_captions(video_path, srt_path)
            if final_video_path:
                results['final_video_path'] = final_video_path
        else:
            print("⚠ Skipping caption burning (SRT file not available)")
        
        # Print summary
        print_summary(results)
        
    except KeyboardInterrupt:
        print("\n\n⚠ Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error during processing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

