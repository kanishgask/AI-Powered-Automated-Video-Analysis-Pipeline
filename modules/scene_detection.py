"""
Scene detection module using OpenCV and SSIM
"""

import cv2
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from skimage.metrics import structural_similarity as ssim
import config
from .utils import format_timestamp_readable, ensure_dir


def detect_scenes(video_path: str, output_dir: Optional[Path] = None) -> List[Dict]:
    """
    Detect scene changes in video using SSIM
    
    Args:
        video_path: Path to video file
        output_dir: Directory to save extracted frames
        
    Returns:
        List of scene change dictionaries with timestamps and frame paths
    """
    try:
        video_path = Path(video_path)
        
        if not video_path.exists():
            print(f"Error: Video file not found - {video_path}")
            return []
        
        if output_dir is None:
            output_dir = config.FRAMES_DIR / video_path.stem
        else:
            output_dir = Path(output_dir)
        
        ensure_dir(output_dir)
        
        print(f"Detecting scenes in: {video_path.name}")
        print("This may take a while for long videos...")
        
        # Open video
        cap = cv2.VideoCapture(str(video_path))
        
        if not cap.isOpened():
            print("Error: Could not open video file")
            return []
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps > 0 else 0
        
        print(f"Video info: {total_frames} frames, {fps:.2f} FPS, {duration:.2f} seconds")
        
        scene_changes = []
        previous_frame = None
        previous_time = 0.0
        frame_count = 0
        scene_index = 0
        
        # Process frames
        while True:
            ret, frame = cap.read()
            
            if not ret:
                break
            
            current_time = frame_count / fps if fps > 0 else 0
            
            # Process every Nth frame based on sample rate
            if frame_count % config.FRAME_SAMPLE_RATE == 0:
                # Convert to grayscale for SSIM comparison
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Resize for faster processing (maintain aspect ratio)
                height, width = gray_frame.shape
                max_dim = 320
                if width > max_dim or height > max_dim:
                    scale = max_dim / max(width, height)
                    new_width = int(width * scale)
                    new_height = int(height * scale)
                    gray_frame = cv2.resize(gray_frame, (new_width, new_height))
                
                # Compare with previous frame
                if previous_frame is not None:
                    # Calculate SSIM
                    similarity = ssim(previous_frame, gray_frame)
                    
                    # Check if scene change detected
                    time_since_last_change = current_time - previous_time
                    
                    if (similarity < config.SCENE_CHANGE_THRESHOLD and 
                        time_since_last_change >= config.MIN_SCENE_DURATION):
                        
                        # Save frame
                        frame_filename = f"scene_{scene_index:04d}_{format_timestamp_readable(current_time).replace(':', '-')}.jpg"
                        frame_path = output_dir / frame_filename
                        
                        cv2.imwrite(str(frame_path), frame)
                        
                        scene_changes.append({
                            'index': scene_index,
                            'timestamp': current_time,
                            'timestamp_readable': format_timestamp_readable(current_time),
                            'frame_path': str(frame_path),
                            'similarity': float(similarity)
                        })
                        
                        print(f"Scene change detected at {format_timestamp_readable(current_time)} "
                              f"(similarity: {similarity:.3f})")
                        
                        previous_time = current_time
                        scene_index += 1
                
                previous_frame = gray_frame.copy()
            
            frame_count += 1
            
            # Progress indicator
            if frame_count % 100 == 0:
                progress = (frame_count / total_frames) * 100
                print(f"Progress: {progress:.1f}% ({frame_count}/{total_frames} frames)")
        
        cap.release()
        
        print(f"Scene detection completed: {len(scene_changes)} scene changes detected")
        return scene_changes
        
    except Exception as e:
        print(f"Error during scene detection: {e}")
        return []


def detect_clicks(video_path: str, scene_changes: List[Dict]) -> List[Dict]:
    """
    Detect UI interactions (clicks/small movements) using frame difference
    
    Args:
        video_path: Path to video file
        scene_changes: List of detected scene changes
        
    Returns:
        List of detected click/interaction dictionaries
    """
    try:
        video_path = Path(video_path)
        
        if not video_path.exists():
            print(f"Error: Video file not found - {video_path}")
            return []
        
        print("Detecting UI interactions (clicks)...")
        
        cap = cv2.VideoCapture(str(video_path))
        
        if not cap.isOpened():
            print("Error: Could not open video file")
            return []
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        clicks = []
        previous_frame = None
        frame_count = 0
        
        # Process frames with higher frequency for click detection
        sample_rate = max(1, int(fps / 10))  # Sample ~10 frames per second
        
        while True:
            ret, frame = cap.read()
            
            if not ret:
                break
            
            current_time = frame_count / fps if fps > 0 else 0
            
            # Sample frames for click detection
            if frame_count % sample_rate == 0:
                # Convert to grayscale
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Resize for faster processing
                height, width = gray_frame.shape
                max_dim = 320
                if width > max_dim or height > max_dim:
                    scale = max_dim / max(width, height)
                    new_width = int(width * scale)
                    new_height = int(height * scale)
                    gray_frame = cv2.resize(gray_frame, (new_width, new_height))
                
                if previous_frame is not None:
                    # Calculate frame difference
                    diff = cv2.absdiff(previous_frame, gray_frame)
                    diff_mean = np.mean(diff)
                    
                    # Check if significant change (but not a scene change)
                    is_scene_change = any(
                        abs(scene['timestamp'] - current_time) < 1.0 
                        for scene in scene_changes
                    )
                    
                    if (diff_mean > config.CLICK_DETECTION_THRESHOLD * 255 and 
                        not is_scene_change):
                        
                        # Check if this is a new click (not too close to previous)
                        is_new_click = True
                        if clicks:
                            last_click_time = clicks[-1]['timestamp']
                            if current_time - last_click_time < 0.5:  # Within 0.5 seconds
                                is_new_click = False
                        
                        if is_new_click:
                            clicks.append({
                                'timestamp': current_time,
                                'timestamp_readable': format_timestamp_readable(current_time),
                                'intensity': float(diff_mean)
                            })
                
                previous_frame = gray_frame.copy()
            
            frame_count += 1
        
        cap.release()
        
        print(f"Click detection completed: {len(clicks)} interactions detected")
        return clicks
        
    except Exception as e:
        print(f"Error during click detection: {e}")
        return []


def extract_key_frames(video_path: str, timestamps: List[float], output_dir: Optional[Path] = None) -> List[str]:
    """
    Extract frames at specific timestamps
    
    Args:
        video_path: Path to video file
        timestamps: List of timestamps in seconds
        output_dir: Directory to save frames
        
    Returns:
        List of paths to extracted frame images
    """
    try:
        video_path = Path(video_path)
        
        if not video_path.exists():
            print(f"Error: Video file not found - {video_path}")
            return []
        
        if output_dir is None:
            output_dir = config.FRAMES_DIR / video_path.stem
        else:
            output_dir = Path(output_dir)
        
        ensure_dir(output_dir)
        
        cap = cv2.VideoCapture(str(video_path))
        
        if not cap.isOpened():
            print("Error: Could not open video file")
            return []
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_paths = []
        
        for timestamp in timestamps:
            frame_number = int(timestamp * fps)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            
            ret, frame = cap.read()
            
            if ret:
                frame_filename = f"frame_{format_timestamp_readable(timestamp).replace(':', '-')}.jpg"
                frame_path = output_dir / frame_filename
                cv2.imwrite(str(frame_path), frame)
                frame_paths.append(str(frame_path))
        
        cap.release()
        return frame_paths
        
    except Exception as e:
        print(f"Error extracting key frames: {e}")
        return []

