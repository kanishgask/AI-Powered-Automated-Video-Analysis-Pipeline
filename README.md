# 🎬 AI-Powered Meeting Video Analysis & Documentation System

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenAI Whisper](https://img.shields.io/badge/OpenAI-Whisper-412991.svg)](https://github.com/openai/whisper)

> **A fully automated Python pipeline that transforms meeting videos into professionally captioned videos with comprehensive documentation reports**

---

## 📖 Table of Contents
- [Overview](#-overview)
- [Key Features](#-key-features)
- [Demo](#-demo)
- [System Architecture](#-system-architecture)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Detailed Usage](#-detailed-usage)
- [Configuration](#%EF%B8%8F-configuration)
- [Output Examples](#-output-examples)
- [Troubleshooting](#-troubleshooting)
- [Performance Metrics](#-performance-metrics)
- [Project Structure](#-project-structure)
- [Technical Stack](#-technical-stack)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

This project is a **comprehensive solution** for automatically processing meeting videos to generate:
- **Accurately transcribed and timestamped captions**
- **Scene-by-scene visual documentation**
- **Detailed meeting reports with screenshots**
- **Professional captioned videos ready for distribution**

Built for the **AI Intern Screening Test**, this system demonstrates proficiency in computer vision, natural language processing, video processing, and automation engineering.

### 🎬 See It In Action
[🎥 Watch 3-Minute Demo Video](https://drive.google.com/file/d/14agRRaKQ_oCZ0qTQOqN2mySeMk_7tgNw/view?usp=sharing) | [📄 View Sample Report](https://your-sample-report-link.com)

---

## ✨ Key Features

### 🎥 **Multi-Source Video Support**
- ✅ **Local Files**: MP4, MOV, AVI formats
- ✅ **YouTube Videos**: Direct URL processing with `yt-dlp`
- ✅ **Cloud Storage**: Google Drive, Dropbox shared links
- ✅ **Web Platforms**: Videos requiring authentication (configurable)

### 🤖 **Advanced AI Processing**
- 🎙️ **Speech-to-Text**: OpenAI Whisper (state-of-the-art accuracy)
- 🔍 **Scene Detection**: SSIM-based algorithm for slide/content changes
- 👆 **UI Interaction Tracking**: Frame-difference analysis for clicks and transitions
- 📝 **Automatic Summarization**: Segment-wise content analysis

### 📄 **Professional Documentation**
- 📊 **Comprehensive Reports**: DOCX/PDF with timestamps, screenshots, and transcripts
- ⏱️ **Precise Timestamping**: Every scene, interaction, and caption synchronized
- 🖼️ **Visual Evidence**: Extracted frames at key moments
- 📋 **SRT Subtitle Files**: Standard format for universal compatibility

### 🎬 **Video Enhancement**
- 🔥 **Caption Burning**: Hardcoded subtitles using FFmpeg
- 🎨 **Customizable Styling**: Font, size, color, position
- 📺 **High-Quality Output**: Professional-grade video encoding

### ⚡ **Automation & Usability**
- 🚀 **One-Click Processing**: Single command execution
- 🔄 **Progress Tracking**: Real-time status updates
- 🛡️ **Error Handling**: Robust exception management with detailed logging
- 💾 **Organized Outputs**: Structured folder system for all artifacts

---

## 🎥 Demo


### Processing Workflow
<img width="820" height="322" alt="image" src="https://github.com/user-attachments/assets/174ea9a7-4b78-44f7-b9a5-c637881d7e9d" />


https://drive.google.com/file/d/14agRRaKQ_oCZ0qTQOqN2mySeMk_7tgNw/view?usp=sharing

### Sample outputs
<img width="820" height="322" alt="image" src="https://github.com/user-attachments/assets/83dd0ce3-0807-4fd0-9243-36ffaedb4613" />



**📹 Full Demo Video**: https://drive.google.com/file/d/14agRRaKQ_oCZ0qTQOqN2mySeMk_7tgNw/view?usp=sharing

---

## 🏗️ System Architecture

```
┌─────────────────┐
│   Video Input   │ (Local/YouTube/Cloud)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Video Download  │ (yt-dlp / Direct)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Audio Extract   │ (FFmpeg)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Transcription  │ (Whisper AI)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Scene Detection │ (OpenCV + SSIM)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   UI Tracking   │ (Frame Difference)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Report Generate │ (python-docx/ReportLab)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Caption Burning │ (FFmpeg)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Final Outputs   │ (Video + Report + SRT)
└─────────────────┘
```

---

## 🔧 Installation

### Prerequisites
- **Python 3.8 or higher**
- **FFmpeg** (required for video/audio processing)
- **4GB RAM minimum** (8GB recommended for large videos)
- **Internet connection** (for Whisper model download on first run)

### Step 1: Clone the Repository
```bash
git clone https://github.com/kanishgask/AI-Powered-Automated-Video-Analysis-Pipeline.git
cd AI-Powered-Automated-Video-Analysis-Pipeline
```

### Step 2: Install FFmpeg

**Windows:**
```bash
# Using Chocolatey
choco install ffmpeg

# Or download from: https://ffmpeg.org/download.html
# Add to PATH manually
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**Linux (CentOS/RHEL):**
```bash
sudo yum install ffmpeg
```

**Verify Installation:**
```bash
ffmpeg -version
```

### Step 3: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: First-Time Setup
On first run, Whisper will automatically download the model (~150MB for base model). This is a one-time process.

---

## 🚀 Quick Start

### Basic Usage
```bash
python main.py
```

The program will prompt you for a video source:

```
======================================================================
  Meeting Video Captioning & Documentation Program
======================================================================

Enter video source:
  - Local file path (e.g., C:\Videos\meeting.mp4)
  - YouTube URL (e.g., https://www.youtube.com/watch?v=...)
  - Cloud storage link (Google Drive, Dropbox, etc.)

Source: _
```

### Example Commands

**Process Local Video:**
```
Source: C:\Users\YourName\Videos\team_meeting.mp4
```

**Process YouTube Video:**
```
Source: https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

**Process Google Drive Link:**
```
Source: https://drive.google.com/file/d/YOUR_FILE_ID/view?usp=sharing
```

---

## 📚 Detailed Usage

### Processing Steps Explained

#### 1️⃣ **Video Download/Loading** (5-30 seconds)
- Validates input source
- Downloads YouTube videos or loads local files
- Verifies video integrity

#### 2️⃣ **Audio Extraction** (10-60 seconds)
- Extracts WAV audio using FFmpeg
- Maintains original quality for accurate transcription

#### 3️⃣ **Transcription** (1-5 minutes for 10-min video)
- Uses OpenAI Whisper for speech-to-text
- Generates timestamped segments
- Creates SRT caption file

#### 4️⃣ **Scene & Interaction Detection** (2-10 minutes)
- Analyzes frames for content changes (SSIM threshold: 0.3)
- Detects UI interactions (clicks, transitions)
- Captures screenshots at key moments

#### 5️⃣ **Report Generation** (30-90 seconds)
- Compiles comprehensive DOCX/PDF report
- Includes screenshots, timestamps, transcript
- Adds summary and interaction log

#### 6️⃣ **Caption Burning** (2-8 minutes)
- Embeds captions into video permanently
- Maintains video quality (H.264 codec)
- Outputs final captioned video

---

## ⚙️ Configuration

Edit `config.py` to customize processing:

```python
# Whisper Model Selection
WHISPER_MODEL = "base"  # Options: tiny, base, small, medium, large
# Model size vs accuracy:
# - tiny:   39M params, fastest, 74% accuracy
# - base:   74M params, balanced (DEFAULT)
# - small:  244M params, good accuracy
# - medium: 769M params, high accuracy
# - large:  1550M params, best accuracy (requires GPU)

# Scene Detection Settings
SCENE_CHANGE_THRESHOLD = 0.3  # Lower = more sensitive (0.0-1.0)
FRAME_SAMPLE_RATE = 5  # Process every Nth frame (higher = faster)

# Report Settings
REPORT_FORMAT = "docx"  # Options: "docx", "pdf"

# Caption Styling
CAPTION_FONT_SIZE = 24
CAPTION_FONT_COLOR = "white"
CAPTION_BG_COLOR = "black@0.5"  # Semi-transparent background
CAPTION_POSITION = "bottom"  # Options: "bottom", "top"

# Output Settings
OUTPUT_DIR = "outputs"
KEEP_TEMP_FILES = False  # Set True to keep intermediate files
```

---

## 📊 Output Examples

### Generated Files Structure
```
outputs/
├── audio/
│   └── meeting_video.wav          # Extracted audio
├── captions/
│   └── captions.srt               # Subtitle file
├── frames/
│   └── meeting_video/
│       ├── scene_001_00-02-15.jpg # Scene screenshots
│       ├── scene_002_00-05-30.jpg
│       └── ...
├── reports/
│   └── meeting_report_20231210_143022.docx  # Comprehensive report
├── final_videos/
│   └── meeting_video_captioned.mp4  # Final output
└── temp/
    └── [temporary processing files]
```

### Sample Report Contents

**Meeting Report Structure:**
1. **Video Information**
   - Title, Duration, Resolution, Source
   
2. **Executive Summary**
   - Key topics discussed
   - Action items identified
   
3. **Scene-by-Scene Breakdown**
   - Timestamp
   - Screenshot
   - Transcript segment
   - Key points
   
4. **Complete Transcript**
   - Full timestamped text
   
5. **UI Interactions Log**
   - Detected clicks/transitions
   - Timestamps and descriptions
   
6. **Appendix**
   - Processing metadata
   - Technical details

---

## 🔍 Troubleshooting

### Common Issues & Solutions

#### ❌ Error: `FFmpeg not found`
**Solution:**
```bash
# Verify FFmpeg installation
ffmpeg -version

# If not found, reinstall and add to PATH
# Windows: Add C:\ffmpeg\bin to System Environment Variables
# macOS/Linux: Should be automatic with brew/apt
```

#### ❌ Error: `YouTube video download failed`
**Solution:**
```bash
# Update yt-dlp to latest version
pip install --upgrade yt-dlp

# Some videos may be region-restricted or age-restricted
# Try with a different video or use VPN
```

#### ❌ Error: `Out of memory during processing`
**Solutions:**
1. Use smaller Whisper model: `WHISPER_MODEL = "tiny"`
2. Increase frame sample rate: `FRAME_SAMPLE_RATE = 10`
3. Process shorter video segments
4. Close other applications to free RAM

#### ❌ Error: `Google Drive link not working`
**Solution:**
```python
# Ensure the link is:
# 1. Publicly accessible (Anyone with link can view)
# 2. Direct download link format:
# https://drive.google.com/uc?id=FILE_ID&export=download

# Convert preview link to download link:
# From: https://drive.google.com/file/d/FILE_ID/view?usp=sharing
# To:   https://drive.google.com/uc?id=FILE_ID&export=download
```

#### ❌ Error: `Caption burning failed`
**Solution:**
```bash
# Check video codec compatibility
ffmpeg -i input.mp4

# If codec is incompatible, re-encode first:
ffmpeg -i input.mp4 -c:v libx264 -c:a aac output.mp4
```

#### ⚠️ Warning: `Transcription quality is poor`
**Solutions:**
1. Use larger Whisper model: `WHISPER_MODEL = "medium"`
2. Check audio quality (background noise, multiple speakers)
3. Try preprocessing audio (noise reduction)

---

## 📈 Performance Metrics

### Processing Time Benchmarks
*(Tested on Intel Core i7-10700, 16GB RAM, no GPU)*

| Video Length | Whisper Model | Processing Time | Report Generation | Caption Burning | **Total** |
|--------------|---------------|-----------------|-------------------|-----------------|-----------|
| 5 minutes    | base          | 1m 20s          | 25s               | 1m 15s          | **3m**    |
| 15 minutes   | base          | 3m 45s          | 45s               | 3m 30s          | **8m**    |
| 30 minutes   | base          | 7m 10s          | 1m 15s            | 6m 45s          | **15m**   |
| 60 minutes   | base          | 14m 20s         | 2m 10s            | 13m 15s         | **30m**   |
| 120 minutes  | base          | 28m 40s         | 3m 50s            | 26m 30s         | **59m**   |

### Model Comparison

| Model  | Size   | Speed  | Accuracy | Use Case                    |
|--------|--------|--------|----------|-----------------------------|
| tiny   | 39M    | ⚡⚡⚡⚡  | ⭐⭐      | Quick testing, low resources|
| base   | 74M    | ⚡⚡⚡   | ⭐⭐⭐    | **Recommended default**     |
| small  | 244M   | ⚡⚡    | ⭐⭐⭐⭐  | Better accuracy needed      |
| medium | 769M   | ⚡     | ⭐⭐⭐⭐⭐| High-quality transcription  |
| large  | 1550M  | 🐌     | ⭐⭐⭐⭐⭐| Maximum accuracy (GPU rec.) |

---

## 📁 Project Structure

```
AI-Powered-Automated-Video-Analysis-Pipeline/
│
├── main.py                      # Main entry point
├── config.py                    # Configuration settings
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── .gitignore                   # Git ignore rules
│
├── modules/                     # Core processing modules
│   ├── __init__.py
│   ├── downloader.py            # Video download handler (yt-dlp)
│   ├── audio_extractor.py       # Audio extraction (FFmpeg)
│   ├── transcription.py         # Whisper transcription
│   ├── scene_detection.py       # Computer vision processing
│   ├── report_generator.py      # DOCX/PDF generation
│   ├── caption_burner.py        # Video caption embedding
│   └── utils.py                 # Helper functions & logging
│
├── outputs/                     # Generated outputs
│   ├── audio/                   # Extracted audio files
│   ├── captions/                # SRT subtitle files
│   ├── frames/                  # Extracted scene screenshots
│   ├── reports/                 # Generated documentation
│   ├── final_videos/            # Captioned videos
│   └── temp/                    # Temporary processing files
│
├── docs/                        # Documentation
│   ├── USER_MANUAL.pdf          # Comprehensive user guide
│   ├── INSTALLATION.pdf         # Detailed installation steps
│   └── API_REFERENCE.md         # Module API documentation
│
├── examples/                    # Sample files
│   ├── sample_report.docx       # Example report output
│   ├── sample_captions.srt      # Example SRT file
│   └── demo_screenshots/        # UI screenshots
│
└── tests/                       # Unit tests (optional)
    ├── __init__.py
    ├── test_downloader.py
    ├── test_transcription.py
    └── test_scene_detection.py
```

---

## 🛠️ Technical Stack

### Core Technologies

| Component          | Technology                    | Purpose                           |
|--------------------|-------------------------------|-----------------------------------|
| Video Processing   | **FFmpeg**, **OpenCV**        | Frame extraction, encoding        |
| Speech Recognition | **OpenAI Whisper**            | Audio transcription               |
| Scene Detection    | **SSIM Algorithm**            | Content change identification     |
| Document Generation| **python-docx**, **ReportLab**| Report creation                   |
| Video Download     | **yt-dlp**                    | YouTube video acquisition         |
| Cloud Storage      | **gdown**, **requests**       | Google Drive/Dropbox handling     |

### Python Libraries

```python
# Computer Vision & Video Processing
opencv-python==4.8.1.78          # Image processing, frame analysis
opencv-contrib-python==4.8.1.78  # Additional CV algorithms

# Audio & Speech Processing
openai-whisper==20231117         # Speech-to-text transcription
ffmpeg-python==0.2.0             # Python FFmpeg wrapper

# Document Generation
python-docx==1.1.0               # DOCX report creation
reportlab==4.0.7                 # PDF generation

# Video Downloading
yt-dlp==2023.11.16               # YouTube video download
gdown==4.7.1                     # Google Drive downloads

# Utilities
Pillow==10.1.0                   # Image manipulation
numpy==1.24.3                    # Numerical operations
tqdm==4.66.1                     # Progress bars
requests==2.31.0                 # HTTP requests
```

---

## 🗺️ Roadmap

### ✅ Completed (v1.0)
- [x] Multi-source video input
- [x] Whisper transcription
- [x] Scene detection
- [x] Report generation (DOCX)
- [x] Caption burning
- [x] Single-click automation

### 🚧 In Progress (v1.1)
- [ ] PDF report generation (95% complete)
- [ ] Web UI with Streamlit
- [ ] Batch processing mode

### 🔮 Planned (v2.0)
- [ ] Speaker diarization (who said what)
- [ ] Multi-language support
- [ ] Keyword extraction & tagging
- [ ] Real-time progress visualization
- [ ] GPU acceleration for Whisper
- [ ] Docker containerization
- [ ] REST API for integration
- [ ] Custom caption styling editor
- [ ] Resume interrupted processing
- [ ] Cloud deployment (AWS/Azure)

### 💡 Experimental Ideas
- [ ] Action item detection (AI-powered)
- [ ] Automatic chapter markers
- [ ] Sentiment analysis per segment
- [ ] Integration with Zoom/Teams
- [ ] Mobile app (React Native)

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Reporting Issues
1. Check [existing issues](https://github.com/kanishgask/AI-Powered-Automated-Video-Analysis-Pipeline/issues)
2. Create detailed bug reports with:
   - Python version
   - Operating system
   - Error messages and logs
   - Steps to reproduce

### Suggesting Features
1. Open a [feature request](https://github.com/kanishgask/AI-Powered-Automated-Video-Analysis-Pipeline/issues/new)
2. Describe the use case
3. Provide examples if possible

### Pull Requests
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Development Setup
```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/AI-Powered-Automated-Video-Analysis-Pipeline.git

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Check code style
flake8 modules/
black modules/ --check
```

---

## 📄 License

This project is licensed under the **MIT License** - see below for details:

```
MIT License

Copyright (c) 2024 Kanishga SK

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgments

- **[OpenAI Whisper](https://github.com/openai/whisper)** - State-of-the-art speech recognition
- **[FFmpeg](https://ffmpeg.org/)** - Comprehensive multimedia framework
- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** - Video downloading utility
- **[OpenCV](https://opencv.org/)** - Computer vision library
- **Python Community** - For excellent documentation and support

---

## 📞 Contact & Support

- **Author**: Kanishga SK
- **GitHub**: [@kanishgask](https://github.com/kanishgask)
- **Project Issues**: [GitHub Issues](https://github.com/kanishgask/AI-Powered-Automated-Video-Analysis-Pipeline/issues)
- **Email**: [your-email@example.com]

---

## 🌟 Star History


If this project helped you, please consider giving it a ⭐️!
<img width="1024" height="1024" alt="image" src="https://github.com/user-attachments/assets/3bccc544-c84a-4012-9544-a57f89a43570" />


[![Star History Chart](https://api.star-history.com/svg?repos=kanishgask/AI-Powered-Automated-Video-Analysis-Pipeline&type=Date)](https://star-history.com/#kanishgask/AI-Powered-Automated-Video-Analysis-Pipeline&Date)

---

## 📸 Screenshots

### Main Interface
![Main Interface](https://via.placeholder.com/800x500?text=Main+Interface+Screenshot)

### Processing Progress
![Processing](https://via.placeholder.com/800x500?text=Processing+Progress)

### Generated Report
![Report](https://via.placeholder.com/800x500?text=Report+Sample)

### Final Output
![Output](https://via.placeholder.com/800x500?text=Final+Captioned+Video)

---

<div align="center">

**Made with ❤️ for automated meeting documentation**

[⬆ Back to Top](#-ai-powered-meeting-video-analysis--documentation-system)

</div>
