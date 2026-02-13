# yt-dlp GUI

A simple graphical user interface for yt-dlp that makes downloading videos and audio easy.

## Features

- **Video/Audio Download**: Download videos and audio from YouTube and other supported platforms
- **Format Selection**: Choose from multiple output formats:
  - Best quality video/audio
  - MP4 (video)
  - MP3 (audio)
  - WAV (audio)
  - M4A (audio)
- **Custom Output Folder**: Select where downloaded files are saved
- **Simple GUI**: User-friendly Tkinter-based interface

## Requirements

- Python 3.x
- yt-dlp
- tkinter (usually included with Python)

## Installation

1. Clone this repository or download the files
2. Install yt-dlp:
   ```bash
   pip install yt-dlp
   ```

## Usage

Run the application:
```bash
python mainGUI.py
```

Then:
1. Enter a video URL
2. Select your desired format from the dropdown
3. Choose an output folder by clicking "Browse"
4. Click "Download" to start

## How It Works

- The GUI uses Tkinter to provide an intuitive interface
- When you click Download, it constructs a yt-dlp command with your selected options
- Downloads are saved to your chosen folder with the video title as the filename
