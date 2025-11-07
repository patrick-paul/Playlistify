# Developer Guide: Using the Smooth UI System

This guide shows developers how to use the new LiveDisplay system for creating smooth, professional terminal UIs in Playlistfy.

---

## Quick Start

### Basic Setup

```python
from playlistfy.ui.theme import Theme
from playlistfy.ui.live_display import LiveDisplay

# Initialize
theme = Theme()
display = LiveDisplay(theme)
```

---

## Common Patterns

### 1. Show a Spinner During an Operation

**Use Case:** Fetching data, waiting for a response, preparing something

```python
with display.spinner_context("Fetching playlist info..."):
    # Your long-running operation here
    playlist_data = fetch_playlist_from_api(url)
    # Spinner automatically clears when done
```

**Result:**
```
⟳ Fetching playlist info...
(Smoothly animates until operation completes, then clears)
```

---

### 2. Show a Progress Bar

**Use Case:** Downloading, processing files, iterating through items

```python
with display.progress_context("Downloading videos") as progress:
    task = progress.add_task("video.mp4", total=100)

    for i in range(100):
        # Do work
        process_chunk()

        # Update progress
        progress.update(task, advance=1)
```

**Result:**
```
  video.mp4 [████████████░░░░] 75% 75/100 bytes 2.5 MB/s 0:00:05
(Updates smoothly in place)
```

---

### 3. Transition from Spinner to Progress

**Use Case:** Operations that have a preparation phase, then trackable progress

```python
def download_task(progress):
    """Callback that receives the progress object"""
    task = progress.add_task("Downloading", total=100)

    for i in range(100):
        # Do the actual work
        download_chunk()
        progress.update(task, advance=1)

# Show spinner during prep, then seamlessly switch to progress
display.transition_spinner_to_progress(
    "Preparing download...",
    download_task
)
```

**Result:**
```
Step 1: ⟳ Preparing download...
        (Spinner for 0.3s)

Step 2: [████████░░░░] 50% Downloading
        (Smooth transition to progress bar)
```

---

### 4. Display Lists with Scroll-In Effect

**Use Case:** Showing playlist videos, search results, file lists

```python
# Build your content
lines = []
for i, video in enumerate(videos, 1):
    lines.append(f"[cyan]{i}.[/cyan] {video['title']}")
    lines.append(f"     [dim]Duration: {video['duration']}[/dim]")
    lines.append("")  # Spacing

# Display with smooth reveal
display.scroll_in_content(lines, delay=0.03)
```

**Result:**
```
  1. Introduction to Python
     Duration: 15:30

  2. Variables and Data Types
     Duration: 22:45

(Each line appears with 30ms delay - readable but not slow)
```

---

### 5. Print Status Messages

**Use Case:** Success/error/warning/info messages

```python
# Success
display.print_status("Download complete!", status="success")
# Output: ✓ Download complete!

# Error
display.print_status("Connection failed", status="error")
# Output: ✗ Connection failed

# Warning
display.print_status("Rate limit approaching", status="warning")
# Output: ⚠ Rate limit approaching

# Info
display.print_status("Processing started", status="info")
# Output: ℹ Processing started
```

---

### 6. Show Section Headers

**Use Case:** Organizing output into clear sections

```python
display.print_section_header("Playlist Videos")
```

**Result:**
```

----------------------------------------
Playlist Videos
----------------------------------------

```

---

### 7. Display Completion Summaries

**Use Case:** Showing results after batch operations

```python
items = [
    {"name": "Video 1", "status": "success", "details": "25.3 MB"},
    {"name": "Video 2", "status": "success", "details": "42.1 MB"},
    {"name": "Video 3", "status": "error", "details": "Network timeout"},
]

display.show_completion_summary("Download Results", items)
```

**Result:**
```
              Download Results
+-----------------------------------------+
| Item    | Status | Details              |
|---------+--------+----------------------|
| Video 1 |   ✓    | 25.3 MB              |
| Video 2 |   ✓    | 42.1 MB              |
| Video 3 |   ✗    | Network timeout      |
+-----------------------------------------+
```

---

## Best Practices

### 1. Always Use Context Managers

**Good:**
```python
with display.spinner_context("Working..."):
    do_work()
# Automatically clears
```

**Bad:**
```python
display.start_spinner("Working...")
do_work()
display.stop_spinner()  # Easy to forget!
```

### 2. Choose the Right Display Method

- **Spinner**: Unknown duration, no progress data
- **Progress Bar**: Known total, can track progress
- **Transition**: Has prep phase, then trackable progress
- **Scroll-In**: Static content that benefits from reveal effect

### 3. Use Appropriate Delays

```python
# Too fast - users can't read
display.scroll_in_content(lines, delay=0.001)  # ❌

# Too slow - feels sluggish
display.scroll_in_content(lines, delay=0.5)    # ❌

# Just right - readable and smooth
display.scroll_in_content(lines, delay=0.03)   # ✅
```

### 4. Provide Clear Messages

**Good:**
```python
with display.spinner_context("Fetching playlist information..."):
    # User knows exactly what's happening
```

**Bad:**
```python
with display.spinner_context("Please wait..."):
    # User doesn't know what they're waiting for
```

### 5. Use Rich Markup for Styling

The LiveDisplay console supports Rich markup:

```python
display.print("[bold cyan]Important![/bold cyan] This is a message")
display.print("[red]Error:[/red] Something went wrong")
display.print("[dim]Secondary information[/dim]")
```

---

## Integration with Existing Components

### In DownloadEngine

```python
class DownloadEngine:
    def __init__(self, theme: Theme, live_display: LiveDisplay = None):
        self.live_display = live_display or LiveDisplay(theme)

    def download_video(self, url: str):
        # Phase 1: Spinner
        with self.live_display.spinner_context("Fetching video info..."):
            info = self.get_video_info(url)

        # Phase 2: Progress
        with self.live_display.progress_context() as progress:
            task = progress.add_task(info['title'], total=100)
            # Download with progress updates
            for chunk in download_chunks(url):
                process_chunk(chunk)
                progress.update(task, advance=chunk_size)

        # Phase 3: Completion
        self.live_display.print_status(
            f"Downloaded: {info['title']}",
            status="success"
        )
```

### In CLI

```python
class CLI:
    def __init__(self):
        self.theme = Theme()
        self.live_display = LiveDisplay(self.theme)
        self.downloader = DownloadEngine(self.theme, self.live_display)

    def show_playlist_videos(self, videos):
        # Use smooth scroll-in for lists
        self.live_display.print_section_header("Available Videos")

        lines = []
        for i, video in enumerate(videos, 1):
            lines.append(f"[cyan]{i}.[/cyan] {video['title']}")
            lines.append(f"     [dim]Duration: {video['duration']}[/dim]")

        self.live_display.scroll_in_content(lines, delay=0.03)
```

---

## Windows Compatibility

The system automatically handles Windows console limitations:

**On Windows:**
- Spinners use ASCII: `|/-\`
- Icons use ASCII: `[OK]`, `[X]`, `[!]`, `[i]`
- Separators use dashes: `----`

**On Linux/Mac:**
- Spinners use Unicode: `⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏`
- Icons use Unicode: `✓`, `✗`, `⚠`, `ℹ`
- Separators use box drawing: `────`

**You don't need to do anything** - it's handled automatically!

---

## Debugging Tips

### 1. Test Your UI Transitions

Create a simple test script:

```python
from playlistfy.ui.theme import Theme
from playlistfy.ui.live_display import LiveDisplay
import time

display = LiveDisplay(Theme())

# Test spinner
with display.spinner_context("Testing spinner..."):
    time.sleep(2)

# Test progress
with display.progress_context() as progress:
    task = progress.add_task("Testing progress", total=100)
    for i in range(100):
        time.sleep(0.05)
        progress.update(task, advance=1)

display.print_status("Tests complete!", status="success")
```

### 2. Check Console Compatibility

```python
# Force check console capabilities
display = LiveDisplay(theme)
print(f"Terminal: {display.console.is_terminal}")
print(f"Legacy Windows: {display.console.legacy_windows}")
print(f"Width: {display.console.width}")
```

### 3. Use transient=True for Temporary Content

```python
# Content disappears after context exits
with Live(content, console=console, transient=True):
    time.sleep(2)
# Content is now gone
```

---

## Advanced Patterns

### Multiple Progress Tasks

```python
with display.progress_context("Downloading playlist") as progress:
    tasks = []

    # Create multiple tasks
    for video in videos:
        task = progress.add_task(video['title'], total=100)
        tasks.append(task)

    # Update them as downloads progress
    for i, task in enumerate(tasks):
        # Download video i
        for chunk in download_video(videos[i]):
            progress.update(task, advance=chunk_size)
```

### Custom Layouts (Advanced)

For complex UIs, you can use Rich's Layout system:

```python
from rich.layout import Layout

# Create sections
layout = Layout()
layout.split_column(
    Layout(name="status"),
    Layout(name="progress"),
    Layout(name="logs")
)

# Update each section independently
# (See Rich documentation for full details)
```

---

## Performance Considerations

### Refresh Rates

```python
# High refresh (10 Hz) for smooth spinners
with Live(spinner, refresh_per_second=10):
    ...

# Lower refresh (4 Hz) for text/panels (less CPU)
with Live(panel, refresh_per_second=4):
    ...
```

### Update Throttling

For very frequent updates, throttle them:

```python
last_update = 0
for chunk in download_chunks():
    current_time = time.time()

    # Only update UI every 100ms
    if current_time - last_update > 0.1:
        progress.update(task, advance=chunk_size)
        last_update = current_time
```

---

## Summary

The LiveDisplay system provides:
- ✅ Smooth, professional UI transitions
- ✅ Easy-to-use context managers
- ✅ Cross-platform compatibility
- ✅ No terminal spam or flickering
- ✅ Rich formatting support

**Remember:** Always use context managers, provide clear messages, and test on multiple platforms!

---

**For More Information:**
- [Rich Documentation](https://rich.readthedocs.io/)
- [test_ui_transitions.py](test_ui_transitions.py) - Working examples
- [UI_IMPROVEMENTS_SUMMARY.md](UI_IMPROVEMENTS_SUMMARY.md) - Full overview
