# Meeting Video Captioning & Documentation Program

A complete Python application that automatically processes meeting videos to extract audio, generate transcriptions, detect scene changes, create detailed reports, and burn captions into videos.

## 🎯 Features

- **Multi-source Video Support**: Process local files (MP4/MOV/AVI), YouTube URLs, or cloud storage links
- **Automatic Transcription**: Uses OpenAI Whisper (open-source) for accurate speech-to-text
- **SRT Caption Generation**: Creates subtitle files with timestamps
- **Scene Detection**: Detects major scene/slide changes using SSIM (Structural Similarity Index)
- **UI Interaction Detection**: Identifies clicks and small movements using frame-difference analysis
- **Comprehensive Reports**: Generates detailed PDF or DOCX reports with screenshots, transcripts, and interaction logs
- **Caption Burning**: Embeds captions directly into the video using FFmpeg
- **One-Command Execution**: Run everything with a single command

## 📋 Requirements

### System Requirements

- **Python 3.8+**
- **FFmpeg** (required for audio extraction and caption burning)
  - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html) or use `choco install ffmpeg`
  - macOS: `brew install ffmpeg`
  - Linux: `sudo apt-get install ffmpeg` or `sudo yum install ffmpeg`

### Python Dependencies

All dependencies are listed in `requirements.txt`. Install them with:

```bash
pip install -r requirements.txt
```

## 🚀 Installation

1. **Clone or download this repository**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install FFmpeg** (if not already installed):
   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt-get install ffmpeg`

4. **Verify FFmpeg installation**:
   ```bash
   ffmpeg -version
   ```

## 📖 Usage

### Basic Usage

Run the main script:

```bash
python main.py
```

The program will prompt you for a video source:
- **Local file**: Enter the full path to your video file (e.g., `C:\Videos\meeting.mp4`)
- **YouTube URL**: Enter the YouTube video URL (e.g., `https://www.youtube.com/watch?v=...`)
- **Cloud storage**: Enter a Google Drive or Dropbox share link

### Example Workflow

```
$ python main.py

======================================================================
  Meeting Video Captioning & Documentation Program
======================================================================

Enter video source:
  - Local file path (e.g., /path/to/video.mp4)
  - YouTube URL (e.g., https://www.youtube.com/watch?v=...)
  - Cloud storage link (Google Drive, Dropbox, etc.)

Source: https://www.youtube.com/watch?v=example

----------------------------------------------------------------------
STEP 1: Downloading/Loading Video
----------------------------------------------------------------------
Downloading YouTube video: https://www.youtube.com/watch?v=example
✓ Video ready: example_video.mp4

----------------------------------------------------------------------
STEP 2: Extracting Audio
----------------------------------------------------------------------
Extracting audio from: example_video.mp4
✓ Audio extracted: example_video.wav

----------------------------------------------------------------------
STEP 3: Transcribing Audio with Whisper
----------------------------------------------------------------------
Loading Whisper model: base
Transcribing audio: example_video.wav
Transcription completed!
✓ SRT file generated: outputs/captions/captions.srt

----------------------------------------------------------------------
STEP 4: Detecting Scene Changes & UI Interactions
----------------------------------------------------------------------
Detecting scenes in: example_video.mp4
Scene change detected at 00:02:15 (similarity: 0.245)
Scene change detected at 00:05:30 (similarity: 0.198)
✓ Scene detection completed: 2 scene changes detected
✓ Click detection completed: 15 interactions detected

----------------------------------------------------------------------
STEP 5: Generating Meeting Report
----------------------------------------------------------------------
Generating DOCX report: outputs/reports/meeting_report_20231201_143022.docx
✓ DOCX report generated

----------------------------------------------------------------------
STEP 6: Burning Captions into Video
----------------------------------------------------------------------
Burning captions into video...
Running FFmpeg (this may take a while)...
✓ Captions burned successfully!

======================================================================
  PROCESSING COMPLETE!
======================================================================
```

## 📂 Project Structure

```
project/
│── main.py                 # Main entry point
│── requirements.txt        # Python dependencies
│── README.md              # This file
│── config.py              # Configuration settings
│
├── modules/
│   ├── __init__.py
│   ├── downloader.py      # Video download handler
│   ├── audio_extractor.py # Audio extraction
│   ├── transcription.py   # Whisper transcription
│   ├── scene_detection.py # Scene & click detection
│   ├── report_generator.py # Report generation
│   ├── caption_burner.py  # Caption burning
│   └── utils.py           # Helper functions
│
└── outputs/
    ├── captions/          # SRT files
    ├── frames/            # Extracted frames
    ├── reports/           # Generated reports
    ├── final_videos/      # Videos with burned captions
    ├── audio/             # Extracted audio files
    └── temp/              # Temporary files
```

## ⚙️ Configuration

Edit `config.py` to customize settings:

- **Whisper Model**: Change `WHISPER_MODEL` to `tiny`, `base`, `small`, `medium`, or `large` (larger = more accurate but slower)
- **Scene Detection**: Adjust `SCENE_CHANGE_THRESHOLD` (0-1, lower = more sensitive)
- **Report Format**: Set `REPORT_FORMAT` to `"docx"` or `"pdf"`
- **Caption Style**: Modify font size, color, and position settings

## 📝 Output Files

After processing, you'll find:

1. **SRT Caption File**: `outputs/captions/captions.srt`
   - Subtitle file with timestamps
   - Can be used with any video player

2. **Meeting Report**: `outputs/reports/meeting_report_YYYYMMDD_HHMMSS.docx` (or `.pdf`)
   - Video information
   - Scene change screenshots with timestamps
   - Full transcript
   - Segmented transcript with timestamps
   - UI interaction log
   - Summary

3. **Extracted Frames**: `outputs/frames/[video_name]/`
   - Screenshots at each detected scene change

4. **Final Video**: `outputs/final_videos/[video_name]_captioned.mp4`
   - Original video with burned-in captions

## 🔧 Troubleshooting

### FFmpeg Not Found

**Error**: `FFmpeg not found`

**Solution**: 
- Install FFmpeg and ensure it's in your system PATH
- Verify with: `ffmpeg -version`

### Whisper Model Download

**First run**: Whisper will download the model (can take a few minutes)

**Solution**: Wait for the download to complete. Models are cached for future use.

### YouTube Download Issues

**Error**: `Error downloading YouTube video`

**Solution**:
- Ensure the URL is valid and the video is accessible
- Some videos may be region-restricted or require authentication
- Update `yt-dlp`: `pip install --upgrade yt-dlp`

### Memory Issues with Large Videos

**Error**: Out of memory during processing

**Solution**:
- Use a smaller Whisper model (`tiny` or `base`)
- Reduce `FRAME_SAMPLE_RATE` in `config.py` to process fewer frames
- Process shorter video segments

### Cloud Storage Links

**Note**: Some cloud storage links (especially Google Drive) may require:
- Public sharing enabled
- Direct download links (not preview links)
- Authentication for private files

## 🎨 Customization

### Change Whisper Model

In `config.py`:
```python
WHISPER_MODEL = "small"  # Options: tiny, base, small, medium, large
```

### Adjust Scene Detection Sensitivity

In `config.py`:
```python
SCENE_CHANGE_THRESHOLD = 0.25  # Lower = more sensitive (detects more changes)
```

### Change Report Format

In `config.py`:
```python
REPORT_FORMAT = "pdf"  # or "docx"
```

## 📊 Performance Notes

- **Transcription**: Depends on video length and Whisper model size
  - `tiny`: Fastest, less accurate
  - `base`: Good balance (default)
  - `large`: Slowest, most accurate

- **Scene Detection**: Processes every Nth frame (configurable)
  - Lower sample rate = faster but may miss some changes

- **Caption Burning**: FFmpeg encoding can take time for long videos
  - Quality settings in `config.py` affect processing time

## 🤝 Contributing

This is a complete, working implementation. Feel free to:
- Report issues
- Suggest improvements
- Submit pull requests

## 📄 License

This project uses open-source libraries. Please refer to individual library licenses:
- Whisper: MIT License
- OpenCV: Apache 2.0
- yt-dlp: Unlicense
- python-docx: MIT License
- ReportLab: BSD License

## 🙏 Acknowledgments

- **OpenAI Whisper** for transcription
- **FFmpeg** for video/audio processing
- **OpenCV** for computer vision
- **yt-dlp** for video downloading

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review error messages for specific guidance
3. Ensure all dependencies are installed correctly

---

**Enjoy automated meeting documentation! 🎉**

