# 🎥 Playlistfy - YouTube Playlist Downloader v2.0

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/patrick-paul/Playlistfy)

> **A beautiful, modern CLI tool for downloading YouTube videos and playlists** - with automatic dependency installation, intelligent error handling, and a Claude Code-inspired interface.

## ✨ What's New in v2.0

- 🎨 **Smooth, Professional UI** - Powered by Rich with controlled transitions and no abrupt changes
- ⏳ **Smart Loading Spinners** - Smooth animations that cleanly transition to progress bars
- 🌊 **Scroll-In Content** - Lists appear with subtle, readable reveal effects
- 📁 **Smart Playlist Folders** - playlists auto-create named folders inside your download directory
- 💾 **"Don't Ask Again" System** - set defaults for quality, directory, parallel mode, and workers
- ⚙️ **Full Settings Menu** - change all preferences without editing config files
- 🔄 **Persistent Session Loop** - download multiple videos/playlists without restarting
- 🚀 **Automatic Dependency Management** - installs yt-dlp, ffmpeg, and all requirements automatically
- 🎯 **Intelligent Error Handling** with actionable suggestions and network error detection
- 📊 **Session Statistics** tracking
- ⚙️ **Configuration System** with support for global and project-level settings
- 🔁 **Smart Retry Logic** with context-aware backoff
- 🌈 **Cross-platform Theme System** (safe ASCII for Windows, Unicode for Linux/Mac)
- 📦 **Modular Architecture** following best practices
- 📝 **Clean Filenames** - video files match actual titles without unnecessary underscores

## 😤 The Problem

You want to download a YouTube playlist. Simple, right? **Wrong.**

- 🚫 **Online tools** require subscriptions or have video limits
- 💸 **Paid software** charges $20-50 for basic functionality
- 🐛 **Broken scripts** require manual ffmpeg installation, PATH configuration, and often fail silently
- ⏰ **Hours wasted** troubleshooting dependencies and cryptic error messages

**I spent 2 hours fighting with tools that don't work.** You shouldn't have to.

## 🚀 Quick Start

### Prerequisites

**Only Python 3.7+ is required.** Everything else installs automatically.

**Don't have Python?** Download it here:

- **Windows**: [Python.org](https://www.python.org/downloads/) - Check "Add Python to PATH" during installation
- **macOS**: [Python.org](https://www.python.org/downloads/) or `brew install python3`
- **Linux**: Usually pre-installed. If not: `sudo apt install python3 python3-pip`

### Installation

#### Option 1: Install as Package (Recommended)

```bash
# Clone the repository
git clone https://github.com/patrick-paul/Playlistfy.git
cd Playlistfy

# Install the package
pip install -e .

# Run from anywhere
playlistfy
```

#### Option 2: Run Directly from Source

```bash
# Clone the repository
git clone https://github.com/patrick-paul/Playlistfy.git
cd Playlistfy

# Run as a module
python -m playlistfy
```

#### Option 3: Use Original v1 Script (Legacy)

```bash
# The original single-file version is in the playlistfy-v1 folder
cd playlistfy-v1
python playlistfy.py
```

That's it! The application will:

- ✓ Check for all dependencies (colorama, tqdm, yt-dlp, rich)
- ✓ Install missing Python packages automatically
- ✓ Check for ffmpeg and offer to install it
- ✓ Guide you through an interactive menu
- ✓ Download videos with progress tracking

## 📖 Features

### 1. **Automatic Dependency Management**

On first run, Playlistfy automatically:

- Installs Python packages (colorama, tqdm, yt-dlp)
- Detects your OS (Windows/Mac/Linux)
- Checks for ffmpeg installation
- Offers to install ffmpeg if missing:
  - **Windows**: via winget, chocolatey, or manual download
  - **macOS**: via Homebrew
  - **Linux**: via apt/dnf/yum/pacman

### 2. **Beautiful Interactive Interface**

```
+--------------------------------------------------------------------------+
| YouTube Playlist Downloader                                              |
| Fast • Reliable • Beautiful                                              |
+--------------------------------------------------------------------------+

-------------------------------- Main Menu --------------------------------

What would you like to do?
* 1. Download single video
* 2. Download playlist
* 3. Settings
* 4. Exit

Enter choice (default: 1)
>
```

### 3. **Download Single Videos**

- Choose quality (best, 1080p, 720p, 480p, or lowest)
- Automatic retry on failure
- Progress tracking with real-time updates
- Option to download multiple videos in sequence

### 4. **Download Entire Playlists**

Features:

- **Loading spinner** shows while fetching playlist metadata
- **Automatic folder creation** - creates a folder named after the playlist inside your download directory
- **List videos** without downloading (preview playlist)
- **Download entire playlist** (all videos)
- **Select video range** (e.g., videos 1-10)
- **Choose specific videos** (comma-separated or ranges like "1,3,5-7")
- **Parallel downloads** for faster downloading (configurable workers)
- **Clean video filenames** - files are named with actual video titles (no underscores)

### 5. **Intelligent Error Handling**

The app analyzes errors and provides actionable suggestions:

```
[X] Error: YouTube detected automated access

Suggestions:
  1. Use --cookies-from-browser chrome
  2. Log into YouTube in your browser first
  3. Wait a few minutes and try again
  4. Use a VPN if you're rate-limited
```

### 6. **Smart Retry Logic**

- Context-aware retry strategies
- Exponential backoff with jitter
- Different retry counts for different error types:
  - Bot detection: 2 attempts with 60s delay
  - Network errors: 5 attempts with 3s delay
  - Other errors: 3 attempts with 5s delay

### 7. **Session Management**

- Persistent session that doesn't exit after each download
- Track download history
- View session statistics
- Return to main menu after each operation

### 8. **"Don't Ask Again" System**

Save time by setting defaults that persist across sessions:

- **Video Quality** - set your preferred quality (best, 1080p, 720p, 480p, worst)
- **Download Directory** - set your default download location
- **Parallel Mode** - choose parallel or sequential downloads
- **Number of Workers** - set how many parallel downloads to run

When you answer these questions, the app will ask if you want to save as default and not be prompted again. You can:

- Re-enable all prompts in Settings
- Change individual defaults in Settings
- Reset everything to factory defaults

### 9. **Full Settings Menu**

Access the Settings menu to:

- View all current settings
- Change video quality default
- Change download directory
- Toggle parallel/sequential download mode
- Change number of parallel workers
- Change max retry attempts
- Re-enable all prompts (if you used "don't ask again")
- Reset all settings to defaults

All settings are automatically saved to `~/.playlistfy/config.json`

### 10. **Configuration System**

Hierarchical configuration support:

1. Defaults (in code)
2. Global config (`~/.playlistfy/config.json`)
3. Project config (`./playlistfy.json`)
4. Environment variables (`PLAYLISTFY_*`)
5. CLI arguments

Example config file:

```json
{
  "output_dir": "downloads",
  "quality": "best",
  "parallel_workers": 3,
  "max_retries": 3,
  "theme": "dark",
  "ask_quality": false,
  "ask_download_dir": false,
  "ask_parallel_mode": false,
  "ask_num_workers": false,
  "use_parallel": true
}
```

## 🛠️ Project Structure

```
Playlistfy/
│
├── pyproject.toml           # Modern Python packaging
├── README.md                # This file
├── LICENSE
│
├── playlistfy-v1/           # v1 reference implementation (DO NOT MODIFY)
│   └── playlistfy.py        # Original single-file version
│
├── src/
│   └── playlistfy/
│       ├── __init__.py      # Package initialization
│       ├── __main__.py      # Entry point
│       ├── cli.py           # Main CLI orchestrator
│       │
│       ├── core/            # Business logic
│       │   ├── downloader.py   # Download engine
│       │   └── playlist.py     # Playlist management
│       │
│       ├── services/        # External integrations
│       │   └── dependencies.py # Dependency management
│       │
│       ├── ui/              # User interface components
│       │   ├── theme.py        # Theme management
│       │   ├── components.py   # Box, Progress, Status
│       │   ├── interactive.py  # Prompts and menus
│       │   └── progress.py     # Enhanced progress display
│       │
│       ├── utils/           # Utilities
│       │   ├── errors.py       # Error handling
│       │   ├── retry.py        # Retry logic
│       │   └── validators.py   # URL validation
│       │
│       └── config/          # Configuration
│           └── settings.py     # Settings management
│
└── downloads/              # Default output directory
```

## 🎨 Architecture

Playlistfy v2.0 follows a clean, modular architecture:

### Core Components

1. **CLI Layer** (`cli.py`): User interaction orchestration
2. **Core Layer** (`core/`): Business logic (downloading, playlist management)
3. **Services Layer** (`services/`): External integrations (yt-dlp, ffmpeg)
4. **UI Layer** (`ui/`): Beautiful terminal interface components with smooth transitions
   - `live_display.py`: Central LiveDisplay manager for all UI updates
   - `progress.py`: Enhanced progress visualization with multi-stage support
   - `components.py`: Box, Progress, and Status components
   - `interactive.py`: User prompts and menus
   - `theme.py`: Cross-platform theme system
5. **Utils Layer** (`utils/`): Cross-cutting concerns (errors, retry, validation)
6. **Config Layer** (`config/`): Configuration management

### Key Design Patterns

- **Dependency Injection**: Components receive dependencies through constructors
- **Observer Pattern**: Progress callbacks for UI updates
- **Strategy Pattern**: Different retry strategies for different error types
- **Factory Pattern**: Theme and component creation
- **Decorator Pattern**: Retry decorator for automatic error handling

## 🔧 Usage Examples

### Basic Usage

```bash
# Install and run
pip install -e .
playlistfy
```

### Download a Single Video

1. Select "Download single video"
2. Enter video URL
3. Choose quality (or use saved default if you enabled "don't ask again")
4. Select output directory (or use saved default if you enabled "don't ask again")
5. See a spinner while video info is being fetched
6. Watch progress bar for download
7. Video is saved with its actual title as the filename

### Download a Playlist

1. Select "Download playlist"
2. Enter playlist URL
3. See a spinner while playlist info is being fetched
4. View playlist information (title, creator, number of videos)
5. Choose from options:
   - List videos only
   - Download entire playlist
   - Select video range (e.g., 1-10)
   - Choose specific videos (e.g., 1,3,5-7)
6. Select quality and parallel workers (or use saved defaults)
7. Playlist creates a folder named after itself inside your download directory
8. Watch progress as videos download
9. All videos are saved with clean filenames in the playlist folder

**Example folder structure after downloading a playlist:**

```
downloads/
└── My Awesome Playlist/
    ├── Video Title One.mp4
    ├── Video Title Two.mp4
    ├── Video Title Three.mp4
    └── ...
```

### Using v1 Script (Legacy)

```bash
# The original single-file version with all features
cd playlistfy-v1
python playlistfy.py

# Supports:
# - Single video download
# - Full playlist download
# - Parallel downloads
# - Quality selection
# - Video range selection
# - Browser cookie authentication
```

See the [Legacy V1 Reference](#-legacy-v1-reference-playlistfypy) section below for detailed information.

## 🎯 Smooth UI/UX System

### Professional Terminal Interface with Rich

Playlistfy v2.0 features a completely redesigned terminal UI powered by [Rich](https://github.com/Textualize/rich), providing smooth, controlled, and professional updates that never feel abrupt or confusing.

### Key UI Principles

**1. No Abrupt Changes**

- Content never appears instantly in a jarring way
- Smooth transitions between different UI states
- Visual continuity that helps users follow what's happening

**2. Controlled Transitions**

- **Spinner → Progress Bar**: When fetching info, you see a smooth spinner that cleanly transitions to a progress bar when download begins
- **Clear State Changes**: Each phase of operation is visually distinct
- **No Text Stacking**: Old content is properly cleared before showing new content

**3. Scroll-In Content Reveals**

- Lists and content appear with a subtle scroll-in effect
- Creates a sense of motion without being slow
- Makes long lists easier to read and follow

**4. Live Updating Regions**

- Progress bars update smoothly in place without spamming the terminal
- Multiple downloads show real-time progress simultaneously
- Status messages update without flickering

**5. Dedicated Display Areas**

- Separate regions for status, progress, and logs
- Interface doesn't jump around as new output arrives
- Professional, organized layout

### UI Transition Examples

**Video Download Flow:**

```
Step 1: Smooth Spinner (fetching)
  ⟳ Fetching video information...

Step 2: Clean Transition to Progress
  [████████████████░░░░] 75% Downloading video.mp4

Step 3: Completion Message
  ✓ Downloaded: video.mp4
```

**Playlist Display with Scroll-In:**

```
Playlist Videos
──────────────────────────
  1. Introduction to Python
     Duration: 15:30

  2. Variables and Data Types
     Duration: 22:45

  (Each line appears with subtle delay)
```

**Parallel Downloads:**

```
  Video 1.mp4 [████████████] 100% ✓ Complete
  Video 2.mp4 [████████░░░░]  65% ↓ 2.1 MB/s
  Video 3.mp4 [███░░░░░░░░░]  25% ↓ 1.8 MB/s
```

### Technical Implementation

**LiveDisplay Manager** ([live_display.py](src/playlistfy/ui/live_display.py))

- Central system for all UI updates
- Uses Rich's Live rendering for flicker-free updates
- Context managers for different display modes
- Windows-compatible with safe ASCII fallbacks

**Smooth Transitions**

- `spinner_context()`: Shows animated spinner during operations
- `progress_context()`: Live-updating progress bars
- `transition_spinner_to_progress()`: Seamlessly switches between states
- `scroll_in_content()`: Controlled content reveals

**Cross-Platform Compatibility**

- Automatically uses safe ASCII characters on Windows
- Unicode symbols on Linux/Mac for enhanced visuals
- No encoding errors or garbled output

**Testing the UI**
Want to see the smooth transitions in action? Run the test suite:

```bash
python test_ui_transitions.py
```

This demonstrates:

- Spinner → Progress bar transitions
- Scroll-in content reveals
- Multiple simultaneous progress bars
- Status message styles
- Completion summaries

### Spinners and Loading States

Never wonder what's happening! The app shows smooth, animated spinners during:

- **Fetching video information** - Clean spinner until video data is ready
- **Fetching playlist information** - Smooth spinner → success message
- **Preparing download** - Brief preparation indication before progress bar

Spinners automatically transition to progress bars when real progress data becomes available.

### Minimal Questions Philosophy

Playlistfy is designed to be **tolerant of mistakes** and **minimal in questions**:

- First-time users are guided through all options
- After you've made choices once, you can save them as defaults
- "Don't ask again" for any setting you don't want to be prompted about
- Settings menu available anytime to change defaults
- Re-enable prompts anytime if you want to be asked again

### Clean Output

- **No duplicate numbers** in video selection lists
- **Clean video filenames** matching actual titles
- **Organized folder structure** for playlists
- **Clear error messages** with actionable suggestions

## 📝 Configuration

### Environment Variables

```bash
export PLAYLISTFY_OUTPUT_DIR="~/Videos"
export PLAYLISTFY_QUALITY="1080p"
export PLAYLISTFY_WORKERS="5"
export PLAYLISTFY_RETRIES="3"
export PLAYLISTFY_THEME="dark"
```

### Global Config File

Create `~/.playlistfy/config.json`:

```json
{
  "output_dir": "~/Videos/YouTube",
  "quality": "best",
  "parallel_workers": 5,
  "max_retries": 3,
  "theme": "dark",
  "prefer_format": "mp4"
}
```

### Project Config File

Create `./playlistfy.json` in your project directory for project-specific settings.

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

### "Rate limited by YouTube" / "Sign in to confirm you're not a bot" (HTTP 429)

**This is the most common issue!** YouTube is blocking automated downloads.

**Solution**: The v1 script (`playlistfy-v1/playlistfy.py`) includes cookie-based authentication:

1. Log into YouTube in your browser (Chrome, Firefox, Edge, etc.)
2. Run `cd playlistfy-v1 && python playlistfy.py`
3. When prompted, select your browser
4. The script will use your login session to bypass bot detection

### Unicode/Encoding Errors on Windows

The v2.0 interface automatically uses safe ASCII characters on Windows to prevent encoding issues.

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Reporting Issues

Found a bug? [Open an issue](https://github.com/patrick-paul/Playlistfy/issues) with:

- Your operating system and Python version
- The full error message
- Steps to reproduce the problem

### Suggesting Features

Have an idea? [Open an issue](https://github.com/patrick-paul/Playlistfy/issues) with:

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
- [ ] Implement video filtering (by duration, views, date)
- [ ] Add audio-only download mode
- [ ] Support for other video platforms (Vimeo, Dailymotion)
- [ ] Export playlist metadata as JSON/CSV
- [ ] GUI interface using rich or textual
- [ ] Docker container for easy deployment
- [ ] Playlist monitoring (download new videos automatically)

## 📜 Important Files

### `playlistfy-v1/playlistfy.py` (v1 - DO NOT MODIFY)

This is the original, working implementation. It serves as:

- **Functional reference** for the v2 implementation
- **Fallback option** if v2 has issues
- **Feature comparison** to ensure nothing is lost

**DO NOT modify or delete this file.** Any new features should be added to the v2 codebase in `src/playlistfy/`.

## 🗂️ Legacy V1 Reference: `playlistfy-v1/playlistfy.py`

### What is playlistfy-v1/playlistfy.py?

`playlistfy-v1/playlistfy.py` is the **original, fully-functional single-file implementation** of Playlistfy (v1). It's a complete, standalone Python script that downloads YouTube videos and playlists without requiring any package installation or project structure.

### Why Does This File Exist?

The v1 file serves multiple important purposes in this project:

1. **Functional Reference**: The v2 modular implementation is built upon the proven logic and patterns from this working v1 script
2. **Fallback Option**: Users who prefer a simple, single-file script can use this instead of the full package
3. **Feature Completeness Guarantee**: Ensures v2 doesn't lose any functionality that existed in v1
4. **Backward Compatibility**: Users who were using the original script don't lose access to it
5. **Development Reference**: Developers can compare v1 and v2 implementations to understand architectural decisions

### Original V1 Features

The legacy v1 file includes all the core features that made Playlistfy useful:

- ✅ **Automatic Dependency Management**: Auto-installs yt-dlp, ffmpeg, colorama, and tqdm
- ✅ **Single Video Downloads**: Download individual YouTube videos with quality selection
- ✅ **Full Playlist Downloads**: Download entire playlists sequentially or in parallel
- ✅ **Video Range Selection**: Download specific ranges (e.g., videos 1-10)
- ✅ **Quality Options**: Choose from best, 1080p, 720p, 480p, or worst quality
- ✅ **Parallel Downloads**: Multi-threaded downloading with configurable workers (1-10)
- ✅ **Progress Tracking**: Real-time progress bars using tqdm
- ✅ **Colored Output**: Beautiful terminal UI using colorama
- ✅ **Cross-Platform**: Works on Windows, macOS, and Linux
- ✅ **Smart ffmpeg Detection**: Checks common installation paths and offers installation help
- ✅ **Browser Cookie Authentication**: Bypass YouTube bot detection using browser cookies
- ✅ **Auto-Retry Logic**: Automatically retries failed downloads with configurable attempts
- ✅ **Error Handling**: Comprehensive error messages with recovery suggestions

### What V2 Inherits from V1

The new modular v2 implementation (in `src/playlistfy/`) builds upon v1's foundation:

| Component                 | V1 Implementation               | V2 Enhancement                                                  |
| ------------------------- | ------------------------------- | --------------------------------------------------------------- |
| **Download Engine**       | Direct yt-dlp subprocess calls  | Abstracted in `core/downloader.py` with improved error handling |
| **Dependency Management** | Inline checks and installations | Centralized in `services/dependencies.py`                       |
| **Progress Display**      | Basic tqdm progress bars        | Enhanced spinners and progress in `ui/progress.py`              |
| **User Interaction**      | Direct input() calls in main()  | Interactive menus in `ui/interactive.py`                        |
| **Configuration**         | Hardcoded constants             | Hierarchical config system in `config/settings.py`              |
| **Error Handling**        | Try-except blocks               | Dedicated error analysis in `utils/errors.py`                   |
| **Retry Logic**           | Basic loop with sleep           | Smart retry strategies in `utils/retry.py`                      |

### Architecture & Workflow (V1)

The v1 script follows a simple monolithic architecture:

```
playlistfy-v1/playlistfy.py (~1160 lines)
│
├── Setup & Imports (lines 1-56)
│   ├── Shebang and docstring
│   ├── Standard library imports
│   └── Auto-install colorama/tqdm if missing
│
├── Global Constants (lines 38-55)
│   ├── Color definitions (GREEN, RED, YELLOW, etc.)
│   └── Emoji/status constants (SUCCESS, ERROR, etc.)
│
├── System Utilities (lines 57-128)
│   ├── get_os() - Detect operating system
│   ├── check_command_exists() - Verify commands in PATH
│   └── verify_ffmpeg_installation() - Comprehensive ffmpeg check
│
├── Dependency Installation (lines 223-449)
│   ├── install_ytdlp() - Install yt-dlp via pip
│   ├── add_to_windows_path() - Add directory to Windows PATH
│   ├── install_ffmpeg_windows() - Windows ffmpeg installation
│   ├── install_ffmpeg_mac() - macOS ffmpeg via Homebrew
│   ├── install_ffmpeg_linux() - Linux ffmpeg via package managers
│   └── setup_dependencies() - Main dependency orchestration
│
├── Playlist Management (lines 528-563)
│   ├── get_playlist_info() - Fetch playlist metadata using yt-dlp
│   └── list_playlist_videos() - Display playlist contents
│
├── Download Functions (lines 564-903)
│   ├── download_single_video() - Download one video with progress
│   ├── download_video_worker() - Worker for parallel downloads
│   ├── download_playlist_parallel() - Multi-threaded playlist download
│   └── download_playlist() - Sequential playlist download
│
└── Main Application (lines 924-1164)
    ├── main() - Interactive CLI menu
    │   ├── Playlist detection
    │   ├── List/Download options
    │   ├── Range selection
    │   ├── Quality selection
    │   └── Worker configuration
    └── Entry point with keyboard interrupt handling
```

**Workflow**:

1. User runs `python playlistfy-v1/playlistfy.py`
2. Script checks and installs dependencies (colorama, tqdm, yt-dlp, ffmpeg)
3. User enters YouTube URL (video or playlist)
4. Script detects URL type and presents appropriate options
5. User selects download preferences (quality, parallel mode, etc.)
6. Script downloads with real-time progress tracking
7. Files saved to specified directory with numbered/titled filenames

### How to Run V1 Manually

The v1 script is completely standalone and easy to use:

```bash
# 1. Navigate to the project directory
cd Playlistfy/playlistfy-v1

# 2. Run the script directly
python playlistfy.py

# That's it! The script will:
# - Check Python version
# - Auto-install colorama and tqdm if needed
# - Auto-install yt-dlp if needed
# - Check for ffmpeg (offer to install if missing)
# - Present an interactive menu
# - Guide you through the download process
```

**No configuration needed.** Just run and follow the prompts.

### When to Use V1 vs V2

**Use V1 (`playlistfy-v1/playlistfy.py`) if you want:**

- 📄 A single file you can copy anywhere and run
- 🚀 Quick, no-setup downloads without package installation
- 🔧 Direct control over yt-dlp command-line options
- 🍪 Browser cookie authentication (built-in support)
- 📦 No pip install needed (just copy and run)

**Use V2 (`playlistfy` package) if you want:**

- 🎨 Modern, beautiful UI with smooth transitions and Rich formatting
- 💾 Settings persistence ("don't ask again" system)
- 📁 Automatic playlist folders with clean filenames
- 🔄 Session management with statistics tracking
- ⚙️ Global configuration files
- 🛠️ Modular, maintainable codebase
- 🚀 Future features and active development

### V1 Maintenance Policy

**Status: FROZEN - Do Not Modify**

The v1 file is intentionally kept unchanged to serve as a stable reference. This policy ensures:

- ✅ Always have a working fallback version
- ✅ Clear comparison point for v2 development
- ✅ No risk of breaking the reference implementation
- ✅ Users who rely on v1 script aren't affected by changes

**All new development happens in v2** (`src/playlistfy/`).

### Example: Using V1 for Bot Detection Issues

One of v1's strengths is built-in browser cookie support, which helps bypass YouTube's bot detection:

```bash
# Run the v1 script
cd playlistfy-v1
python playlistfy.py

# When downloading a single video:
# 1. Enter your video URL
# 2. Select quality
# 3. Choose browser (Chrome, Firefox, Edge, Brave, Opera)
# 4. Script uses your browser's logged-in session
# 5. Successfully bypass bot detection!

# Make sure you're logged into YouTube in your chosen browser first
```

This feature is especially useful when encountering HTTP 429 (rate limiting) errors.

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

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - The amazing YouTube downloader
- [ffmpeg](https://ffmpeg.org/) - The multimedia framework
- [colorama](https://github.com/tartley/colorama) - Cross-platform colored terminal text
- [tqdm](https://github.com/tqdm/tqdm) - Progress bars
- [Rich](https://github.com/Textualize/rich) - Beautiful terminal formatting
- [Claude Code](https://claude.com/claude-code) - UI/UX inspiration

## 📊 Project Stats

- **Version**: 2.0.0
- **Lines of Code**: ~2500+ (modular architecture with smooth UI system)
- **Dependencies**: 4 (auto-installed: colorama, tqdm, yt-dlp, rich)
- **Platforms Supported**: Windows, macOS, Linux
- **UI System**: Rich-powered with controlled transitions
- **Time Saved**: Hours of your life

---

**Made with 😤 frustration and ☕ coffee after wasting 2 hours on tools that don't work.**

**If this saved you time, give it a ⭐ and share it with others!**

## 📬 Contact

Questions? Suggestions? Found a bug?

- Open an issue: [GitHub Issues](https://github.com/patrick-paul/Playlistfy/issues)
- Discussions: [GitHub Discussions](https://github.com/patrick-paul/Playlistfy/discussions)

---

**Remember**: Your time is valuable. Don't waste it on broken tools. 🚀
