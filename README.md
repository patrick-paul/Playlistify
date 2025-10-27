# 🎥 Playlistify - YouTube Playlist Downloader

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/patrick-paul/Playlistify)

> **Stop wasting time with broken tools and paid services.** Download entire YouTube playlists with one command - completely free and automatic.

## 😤 The Problem

You want to download a YouTube playlist. Simple, right? **Wrong.**

- 🚫 **Online tools** require subscriptions or have video limits
- 💸 **Paid software** charges $20-50 for basic functionality
- 🐛 **Broken scripts** require manual ffmpeg installation, PATH configuration, and often fail silently
- ⏰ **Hours wasted** troubleshooting dependencies and cryptic error messages

**I spent 2 hours fighting with tools that don't work.** You shouldn't have to.

## ✨ The Solution

**Playlistify** is a Python script that:
- ✅ **Works immediately** - auto-installs all dependencies
- ✅ **100% free** - no subscriptions, no limits
- ✅ **Cross-platform** - Windows, macOS, Linux
- ✅ **Smart** - detects your OS and configures everything automatically
- ✅ **No manual setup** - installs yt-dlp, ffmpeg, and adds to PATH automatically

## 🚀 Quick Start

### Prerequisites

**Only Python 3.7+ is required.** Everything else installs automatically.

**Don't have Python?** Download it here:
- **Windows**: [Python.org](https://www.python.org/downloads/) - Check "Add Python to PATH" during installation
- **macOS**: [Python.org](https://www.python.org/downloads/) or `brew install python3`
- **Linux**: Usually pre-installed. If not: `sudo apt install python3 python3-pip`

### Installation

1. **Clone or download this repository:**
   ```bash
   git clone https://github.com/patrick-paul/Playlistify.git
   cd Playlistify
   ```

2. **Run the script:**
   ```bash
   python playlist_downloader.py
   ```

That's it! The script will:
- ✓ Check for yt-dlp (auto-install if missing)
- ✓ Check for ffmpeg (auto-install if missing)
- ✓ Add ffmpeg to PATH (Windows)
- ✓ Ask for your playlist URL
- ✓ Download all videos as MP4 files

### Usage Example

```bash
$ python playlist_downloader.py

==================================================
YouTube Playlist Downloader
==================================================

Checking dependencies...
==================================================

Detected OS: windows

[1/2] Checking yt-dlp...
  ✓ yt-dlp is already installed
  ✓ Updated to latest version

[2/2] Checking ffmpeg...
  ✗ ffmpeg not found
  Install ffmpeg now? (y/n): y
  Downloading ffmpeg manually...
  ✓ ffmpeg installed to C:\Users\YourName\ffmpeg
  ✓ Added to PATH

==================================================
Setup complete!
==================================================

Enter YouTube playlist URL: https://www.youtube.com/playlist?list=...

What would you like to do?
1. List all videos (no download)
2. Download entire playlist
3. Download with custom quality

Enter choice (1-3): 2
Enter output directory (default: downloads): 

Downloading playlist to: downloads
Quality: best
--------------------------------------------------
[download] Downloading item 1 of 50
...
```

## 📖 Features

### 1. **List Videos Without Downloading**
Preview all videos in a playlist with titles, URLs, and durations:
```
1. Introduction to Python
   URL: https://www.youtube.com/watch?v=... | Duration: 15:30

2. Variables and Data Types
   URL: https://www.youtube.com/watch?v=... | Duration: 22:45
```

### 2. **Download Entire Playlists**
Download all videos in the best available quality with a single command.

### 3. **Custom Quality Options**
Choose your preferred quality:
- `best` - Highest quality available (default)
- `1080p` - Full HD
- `720p` - HD
- `480p` - Standard Definition
- `worst` - Lowest quality (smallest file size)

### 4. **Smart Features**
- **Resume downloads** - Interrupted? Just run again, it continues where it left off
- **Error handling** - Skips failed videos and continues with the rest
- **Clean filenames** - `001 - Video_Title.mp4`, `002 - Another_Video.mp4`
- **Auto-merge** - Combines video and audio into single MP4 files

## 🛠️ How It Works

### Dependencies (Auto-Installed)

1. **yt-dlp** - Modern YouTube downloader (fork of youtube-dl)
   - Installed via: `pip install yt-dlp`
   - Handles YouTube's anti-bot measures
   - Actively maintained with frequent updates

2. **ffmpeg** - Video/audio processing
   - **Windows**: Downloads from gyan.dev or via winget/chocolatey
   - **macOS**: Installed via Homebrew
   - **Linux**: Installed via apt/yum/dnf/pacman
   - Required to merge video and audio streams

### Technical Details

- Downloads highest quality video and audio streams separately
- Uses ffmpeg to merge them into a single MP4 file
- Automatically handles rate limiting from YouTube
- Supports playlists of any size (tested with 200+ videos)
- Downloads are saved with playlist order: `001 - Title.mp4`, `002 - Title.mp4`, etc.

## 🐛 Troubleshooting

### "Python is not recognized as a command"
- **Windows**: Reinstall Python and check "Add Python to PATH"
- **macOS/Linux**: Use `python3` instead of `python`

### "ffmpeg installation failed"
Install manually:
- **Windows**: [Download ffmpeg](https://www.gyan.dev/ffmpeg/builds/) and add to PATH
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg` (Ubuntu/Debian)

### "Videos download as separate .webm files"
ffmpeg is not installed or not in PATH. Run the script again and choose to install ffmpeg when prompted.

### "WARNING: nsig extraction failed"
This is normal. YouTube is making it harder to download, but yt-dlp handles it. Videos will still download successfully.

### "Rate limited by YouTube"
The script automatically adds delays between downloads. If this persists:
- Wait a few hours before trying again
- Use a VPN to change your IP address
- Update yt-dlp: `pip install --upgrade yt-dlp`

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Reporting Issues
Found a bug? [Open an issue](https://github.com/patrick-paul/Playlistify/issues) with:
- Your operating system and Python version
- The full error message
- Steps to reproduce the problem

### Suggesting Features
Have an idea? [Open an issue](https://github.com/patrick-paul/Playlistify/issues) with:
- Description of the feature
- Why it would be useful
- How it might work

### Pull Requests
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test on your platform
5. Submit a pull request

### Ideas for Contributions
- [ ] Add subtitle download support
- [ ] Implement parallel downloads for faster speed
- [ ] Add GUI interface
- [ ] Support for other video platforms (Vimeo, Dailymotion, etc.)
- [ ] Download specific video ranges (e.g., videos 10-20)
- [ ] Filter by duration (e.g., only videos under 10 minutes)
- [ ] Add progress bar for individual video downloads
- [ ] Export playlist metadata as JSON/CSV
- [ ] Support for member-only content (cookies authentication)
- [ ] Automatic retry on failed downloads

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Legal Disclaimer

This tool is for **personal use only**. Please respect copyright laws and YouTube's Terms of Service:
- Only download videos you have permission to download
- Don't redistribute downloaded content without permission
- Don't use this tool for piracy or commercial purposes
- Some content may be protected by copyright

**Use responsibly and ethically.**

## 🙏 Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - The amazing YouTube downloader that makes this possible
- [ffmpeg](https://ffmpeg.org/) - The multimedia framework that powers video processing
- Everyone who spent hours troubleshooting broken tools - this is for you

## 📊 Project Stats

- **Lines of Code**: ~400
- **Dependencies**: 2 (auto-installed)
- **Platforms Supported**: 3 (Windows, macOS, Linux)
- **Time Saved**: Hours of your life

---

**Made with 😤 frustration and ☕ coffee after wasting 2 hours on tools that don't work.**

If this saved you time, give it a ⭐ and share it with others!

## 📬 Contact

Questions? Suggestions? Found a bug?
- Open an issue: [GitHub Issues](https://github.com/patrick-paul/Playlistify/issues)
- Discussions: [GitHub Discussions](https://github.com/patrick-paul/Playlistify/discussions)

---

**Remember**: Your time is valuable. Don't waste it on broken tools. 🚀
