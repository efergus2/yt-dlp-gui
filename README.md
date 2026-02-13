# yt-dlp GUI

A simple graphical user interface for yt-dlp that makes downloading videos and audio easy.

## Features

- **Video/Audio Download**: Download from YouTube and all platforms supported by yt-dlp.
- **Format Selection**: Pick one of the common output types:
  - `best` (highest quality video + audio)
  - MP4 (video)
  - MP3, WAV, M4A (audio-only)
- **Custom Output Folder**: Browse and save files wherever you like.
- **Update Button**: Click "Update yt-dlp" to fetch the latest version via pip.
- **Clear Log**: Quickly erase the log window when it fills up.
- **Lightweight**: Built with `customtkinter` on top of tkinter for a modern dark theme.

## Requirements

- Python 3.7+ (3.10+ recommended)
- `yt-dlp` installed in the same environment (`pip install yt-dlp`)
- `tkinter` (bundled with most CPython distributions)
- `customtkinter` for the styled widgets (`pip install customtkinter`)

## Installation

1. Clone this repository or download the files locally.
2. Create/activate a virtual environment (optional but recommended):
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate     # Windows
   source .venv/bin/activate      # macOS/Linux
   ```
3. Install dependencies:
   ```bash
   pip install yt-dlp customtkinter
   ```

## Usage

Run the application:
```bash
python mainGUI.py
```

Steps:

1. Paste or type the video/audio URL in the top field.
2. Select the output format from the dropdown.
3. Click **Browse** to choose a destination directory.
4. Press **Download**. Progress and yt-dlp messages will appear in the log.
5. Optionally update yt-dlp from the sidebar and clear the log when needed.

> ⚠️ Make sure the output folder exists and yt-dlp is installed. The app will display warnings if either check fails.

## How It Works

The script defines a single `YTDLP_GUI` class derived from `CTk` (CustomTkinter). When you interact with the controls:

- `start_download` spawns a daemon thread so the interface remains responsive.
- The download thread builds a command line, checks for basic errors, and streams output from `yt-dlp`.
- Regular expressions are used to parse progress percentages and update a progress bar.
- `update_ytdlp` runs pip in a subprocess to ensure yt-dlp stays current.

The logfile area captures all output so you can review or copy details if something goes wrong.

The entire application is contained in `mainGUI.py`; no additional configuration is required.
