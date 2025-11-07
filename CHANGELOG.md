# Playlistfy Changelog

## [2.0.0] - 2025

### Major Changes

#### File Structure Reorganization

- **V1 Script Relocated**: The original single-file implementation has been moved to `playlistfy-v1/` folder
  - Old location: `playlist_downloader.py` (root directory)
  - New location: `playlistfy-v1/playlistfy.py`
  - File header updated to reflect new location and V2 improvements
  - Code remains unchanged and frozen for reference purposes

#### Smooth UI System (NEW)

- **Rich Integration**: Added Rich library for professional terminal formatting

  - Automatic dependency checking and installation
  - Smooth spinner → progress bar transitions
  - Scroll-in content reveals for lists
  - Cross-platform compatibility (Windows/Mac/Linux)
  - Safe ASCII fallbacks for Windows console

- **LiveDisplay Manager**: New centralized UI update system

  - `src/playlistfy/ui/live_display.py` - 348 lines of smooth UI magic
  - Flicker-free live updates
  - Context managers for different display modes
  - No terminal spam or buffer flooding

- **Enhanced Components**:
  - Updated `src/playlistfy/ui/progress.py` with LiveDisplay integration
  - Updated `src/playlistfy/core/downloader.py` with 3-phase download flow
  - Updated `src/playlistfy/cli.py` with LiveDisplay throughout
  - Updated `src/playlistfy/services/dependencies.py` to auto-install Rich

#### New Test Suites

- `test_ui_transitions.py` - Demonstrates all UI transitions
- `test_dependencies.py` - Verifies dependency system works correctly

#### Documentation Updates

- **README.md**: Updated all references to reflect new v1 location

  - Changed `playlist_downloader.py` → `playlistfy-v1/playlistfy.py`
  - Added comprehensive UI/UX documentation
  - Updated dependency list to include Rich

- **New Documentation**:
  - `UI_IMPROVEMENTS_SUMMARY.md` - Complete UI system overview
  - `DEVELOPER_UI_GUIDE.md` - Developer reference for LiveDisplay API
  - `CHANGELOG.md` - This file

### Breaking Changes

#### File Location Changes

Users need to update their workflows:

**Before:**

```bash
python playlist_downloader.py
```

**After:**

```bash
# V2 (Recommended)
pip install -e .
playlistfy

# V1 (Legacy)
cd playlistfy-v1
python playlistfy.py
```

#### New Dependency

- Rich (>= 13.0.0) is now required
- Automatically installed on first run
- No manual action needed

### Features Added

1. **Smooth UI Transitions**

   - Spinner animations while loading
   - Clean transition to progress bars
   - No abrupt content changes

2. **Scroll-In Content**

   - Playlist videos appear with controlled timing
   - Readable reveal effect (30-50ms delays)
   - Professional presentation

3. **Live Updating Regions**

   - Progress bars update in place
   - Multiple downloads show simultaneously
   - Dedicated status/progress/log areas

4. **Cross-Platform Polish**

   - Windows: Safe ASCII characters
   - Linux/Mac: Unicode symbols
   - Zero encoding errors

5. **Automatic Dependency Management**
   - Rich added to auto-check system
   - Installs alongside colorama, tqdm, yt-dlp
   - ffmpeg installation assistance

### Technical Improvements

1. **Architecture**

   - Clean separation of UI concerns
   - Reusable LiveDisplay context managers
   - Modular component system

2. **Performance**

   - Efficient refresh rates (4-10 Hz)
   - Minimal CPU usage
   - Optimized for standard terminals

3. **Code Quality**
   - Type hints throughout
   - Comprehensive docstrings
   - Test coverage for UI and dependencies

### Migration Guide

#### For End Users

**No action required!** Just update and run:

```bash
cd Playlistfy
git pull
pip install -e .
playlistfy
```

The app will automatically:

- Install Rich if missing
- Show the new smooth UI
- Work exactly as before (but prettier!)

#### For Developers

**File References:**

- Update any scripts referencing `playlist_downloader.py` to `playlistfy-v1/playlistfy.py`
- V1 remains unchanged - safe to reference for comparison

**Using LiveDisplay:**

```python
from playlistfy.ui.live_display import LiveDisplay
from playlistfy.ui.theme import Theme

display = LiveDisplay(Theme())

# Smooth spinner
with display.spinner_context("Loading..."):
    # Long operation

# Progress bar
with display.progress_context() as progress:
    task = progress.add_task("Working", total=100)
    # Update progress
```

See `DEVELOPER_UI_GUIDE.md` for complete API reference.

### Known Issues

None currently reported.

### Credits

- **UI System**: Powered by [Rich](https://github.com/Textualize/rich)
- **Inspiration**: Claude Code terminal interface
- **Testing**: Windows 11, cross-compatible with macOS and Linux

---

## [1.0.0] - Previous

Original single-file implementation (now in `playlistfy-v1/playlistfy.py`)

### Features

- Single video downloads
- Playlist downloads (parallel/sequential)
- Browser cookie authentication
- Automatic dependency installation
- Cross-platform support
- Quality selection
- Video range selection

---

**Note**: The v1 file is frozen and will not receive updates. All new features are added to v2.
