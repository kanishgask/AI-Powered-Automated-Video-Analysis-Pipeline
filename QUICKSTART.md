# Quick Start Guide

## 🚀 How to Run the Project

### Step 1: Install Python Dependencies

Open a terminal/command prompt in the project directory and run:

```bash
pip install -r requirements.txt
```

**Note**: If you're using Python 3, you might need to use `pip3` instead of `pip`.

### Step 2: Install FFmpeg

FFmpeg is required for audio extraction and caption burning. Install it based on your operating system:

#### Windows:
1. Download FFmpeg from: https://ffmpeg.org/download.html
2. Extract the zip file
3. Add FFmpeg to your system PATH:
   - Copy the path to the `bin` folder (e.g., `C:\ffmpeg\bin`)
   - Add it to System Environment Variables → Path
4. Verify installation:
   ```bash
   ffmpeg -version
   ```

**Alternative for Windows (using Chocolatey):**
```bash
choco install ffmpeg
```

#### macOS:
```bash
brew install ffmpeg
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

#### Linux (CentOS/RHEL):
```bash
sudo yum install ffmpeg
```

### Step 3: Run the Program

Simply execute:

```bash
python main.py
```

Or if you need to use Python 3 explicitly:

```bash
python3 main.py
```

### Step 4: Provide Video Source

When prompted, enter one of the following:

1. **Local File Path**:
   ```
   C:\Videos\meeting.mp4
   ```
   or on Mac/Linux:
   ```
   /home/user/videos/meeting.mp4
   ```

2. **YouTube URL**:
   ```
   https://www.youtube.com/watch?v=VIDEO_ID
   ```

3. **Cloud Storage Link** (Google Drive, Dropbox, etc.):
   ```
   https://drive.google.com/file/d/FILE_ID/view
   ```

### Example Run

```
$ python main.py

======================================================================
  Meeting Video Captioning & Documentation Program
======================================================================

Enter video source:
  - Local file path (e.g., /path/to/video.mp4)
  - YouTube URL (e.g., https://www.youtube.com/watch?v=...)
  - Cloud storage link (Google Drive, Dropbox, etc.)

Source: meeting_video.mp4

----------------------------------------------------------------------
STEP 1: Downloading/Loading Video
----------------------------------------------------------------------
Copying local file: meeting_video.mp4
File copied to: outputs/temp/meeting_video.mp4
✓ Video ready: meeting_video.mp4

----------------------------------------------------------------------
STEP 2: Extracting Audio
----------------------------------------------------------------------
Extracting audio from: meeting_video.mp4
Audio extracted: outputs/audio/meeting_video.wav
✓ Audio extracted: meeting_video.wav

----------------------------------------------------------------------
STEP 3: Transcribing Audio with Whisper
----------------------------------------------------------------------
Loading Whisper model: base
Note: First run will download the model (this may take a few minutes)
Transcribing audio: meeting_video.wav
This may take a while depending on audio length...
Transcription completed!
Generating SRT file: outputs/captions/captions.srt
SRT file generated: outputs/captions/captions.srt
✓ SRT file generated: captions.srt

----------------------------------------------------------------------
STEP 4: Detecting Scene Changes & UI Interactions
----------------------------------------------------------------------
Detecting scenes in: meeting_video.mp4
This may take a while for long videos...
Video info: 1800 frames, 30.00 FPS, 60.00 seconds
Scene change detected at 00:02:15 (similarity: 0.245)
Scene change detected at 00:05:30 (similarity: 0.198)
Progress: 100.0% (1800/1800 frames)
Scene detection completed: 2 scene changes detected
Detecting UI interactions (clicks)...
Click detection completed: 15 interactions detected
✓ Scene detection: 2 scene changes detected
✓ UI interactions: 15 interactions detected

----------------------------------------------------------------------
STEP 5: Generating Meeting Report
----------------------------------------------------------------------
Generating DOCX report: outputs/reports/meeting_report_20231201_143022.docx
DOCX report generated: outputs/reports/meeting_report_20231201_143022.docx
✓ Report generated: meeting_report_20231201_143022.docx

----------------------------------------------------------------------
STEP 6: Burning Captions into Video
----------------------------------------------------------------------
Burning captions into video...
Input: meeting_video.mp4
SRT: captions.srt
Output: meeting_video_captioned.mp4
Running FFmpeg (this may take a while)...
✓ Captions burned successfully!
  Output: outputs/final_videos/meeting_video_captioned.mp4
  Size: 45.32 MB

======================================================================
  PROCESSING COMPLETE!
======================================================================

📁 Output directory: outputs
  ├── Captions: outputs/captions
  ├── Frames: outputs/frames
  ├── Reports: outputs/reports
  └── Final Videos: outputs/final_videos

📄 SRT File: outputs/captions/captions.srt
📄 Report: outputs/reports/meeting_report_20231201_143022.docx
🎬 Final Video: outputs/final_videos/meeting_video_captioned.mp4
```

## 📁 Output Files Location

All generated files are saved in the `outputs/` directory:

- **Captions**: `outputs/captions/captions.srt`
- **Extracted Frames**: `outputs/frames/[video_name]/`
- **Reports**: `outputs/reports/meeting_report_YYYYMMDD_HHMMSS.docx` (or `.pdf`)
- **Final Videos**: `outputs/final_videos/[video_name]_captioned.mp4`
- **Audio Files**: `outputs/audio/[video_name].wav`

## ⚠️ Troubleshooting

### "FFmpeg not found" Error

**Solution**: Make sure FFmpeg is installed and in your system PATH. Verify with:
```bash
ffmpeg -version
```

### "Module not found" Error

**Solution**: Install missing dependencies:
```bash
pip install -r requirements.txt
```

### Whisper Model Download

On first run, Whisper will download the model (can take a few minutes). This is normal and only happens once per model size.

### YouTube Download Issues

- Ensure the URL is correct and the video is publicly accessible
- Some videos may be region-restricted
- Update yt-dlp: `pip install --upgrade yt-dlp`

### Memory Issues

For very long videos, you might encounter memory issues. Solutions:
- Use a smaller Whisper model (edit `config.py`: `WHISPER_MODEL = "tiny"`)
- Process shorter video segments

## 🎯 Quick Test

To test if everything is set up correctly:

1. Create a short test video (or use any existing video)
2. Run: `python main.py`
3. Enter the video path when prompted
4. Wait for processing to complete
5. Check the `outputs/` folder for results

## 💡 Tips

- **First Run**: The first time you run the program, Whisper will download the model. This can take 5-10 minutes depending on your internet speed.
- **Processing Time**: 
  - Transcription: ~1-2x video duration (depends on model size)
  - Scene detection: ~0.5-1x video duration
  - Caption burning: ~0.5-1x video duration
- **Model Selection**: Edit `config.py` to change Whisper model:
  - `tiny`: Fastest, less accurate
  - `base`: Good balance (default)
  - `large`: Slowest, most accurate

---

**That's it! You're ready to process meeting videos! 🎉**


