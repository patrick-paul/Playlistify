"""
Enhanced progress visualization with multi-stage support
"""
import sys
import time
from typing import List, Dict, Optional, Generator, Callable
from dataclasses import dataclass
from contextlib import contextmanager
import shutil
from rich.progress import Progress as RichProgress, TaskID
from .theme import Theme
from .live_display import LiveDisplay

@dataclass
class DownloadStage:
    """Represents a stage in the download process"""
    name: str
    progress: float = 0.0
    speed: Optional[str] = None
    eta: Optional[str] = None
    status: str = 'waiting'
    message: Optional[str] = None

class EnhancedProgress:
    """Advanced progress visualization with multi-stage support using LiveDisplay"""

    def __init__(self, theme: Theme, live_display: Optional[LiveDisplay] = None):
        self.theme = theme
        self.live_display = live_display or LiveDisplay(theme)
        self.term_width = shutil.get_terminal_size().columns
        self._last_update = 0
        self._spinner_idx = 0
    
    def download_with_stages(self, title: str, stages: List[DownloadStage], 
                           width: int = 50) -> None:
        """
        Show multi-stage download progress
        Example:
        [1/42] Introduction to Python.mp4
        ├─ Download video   ████████████████████ 100% (125.3 MB) [2.5 MB/s]
        ├─ Download audio   ████████████████████ 100% (8.2 MB)   [1.1 MB/s]
        └─ Merging streams  ████████░░░░░░░░░░░░  45% [ETA: 12s]
        """
        # Title
        print(self.theme.apply_color(title, 'text'))
        
        # Progress for each stage
        for i, stage in enumerate(stages):
            # Tree characters
            if i == len(stages) - 1:
                prefix = '└─'
            else:
                prefix = '├─'
            
            # Progress bar
            progress = int(stage.progress * width)
            bar = '█' * progress + '░' * (width - progress)
            percent = f"{stage.progress * 100:3.0f}%"
            
            # Status info
            info = []
            if stage.speed:
                info.append(f"↓ {stage.speed}")
            if stage.eta:
                info.append(f"ETA: {stage.eta}")
            status = f" [{', '.join(info)}]" if info else ""
            
            # Color based on status
            if stage.status == 'completed':
                color = 'success'
            elif stage.status == 'error':
                color = 'error'
            else:
                color = 'primary'
            
            line = (
                f"{prefix} {stage.name:<15} "
                f"{self.theme.apply_color(bar, color)} "
                f"{percent}{status}"
            )
            
            if stage.status == 'error' and stage.message:
                line += f"\n    {self.theme.apply_color('✗ ' + stage.message, 'error')}"
            
            print(line)
    
    def parallel_downloads(self, tasks: List[Dict], overall_progress: float) -> None:
        """
        Show parallel download progress
        Example:
        Downloading 3 videos in parallel
        ────────────────────────────────────────────────────────
        [01] Video 1 ████████████░░░░░░░░  65% ↓ 2.1 MB/s
        [02] Video 2 ████░░░░░░░░░░░░░░░░  25% ↓ 1.8 MB/s
        [03] Video 3 ████████████████████ 100% ✓ Complete
        
        Overall: 42/120 videos (35%) [Est. 45m remaining]
        """
        width = min(self.term_width - 40, 50)  # Leave room for text
        
        # Individual task progress
        for task in tasks:
            index = task.get('index', '??')
            title = task.get('title', 'Unknown')[:30]
            progress = task.get('progress', 0.0)
            speed = task.get('speed', '')
            status = task.get('status', 'downloading')
            
            # Progress bar
            bar_width = int(progress * width)
            bar = '█' * bar_width + '░' * (width - bar_width)
            
            # Status indicator
            if status == 'completed':
                status_icon = self.theme.apply_color('✓', 'success')
            elif status == 'error':
                status_icon = self.theme.apply_color('✗', 'error')
            else:
                status_icon = self.theme.apply_color('↓', 'primary')
            
            line = (
                f"[{index:02d}] {title:<30} "
                f"{self.theme.apply_color(bar, 'primary')} "
                f"{progress*100:3.0f}% {status_icon} "
            )
            
            if speed and status == 'downloading':
                line += f"{speed}/s"
            elif status == 'error':
                line += self.theme.apply_color('Failed', 'error')
            elif status == 'completed':
                line += self.theme.apply_color('Complete', 'success')
            
            print(line)
        
        # Overall progress
        total_width = self.term_width - 10
        overall_bar_width = int(overall_progress * total_width)
        overall_bar = '█' * overall_bar_width + '░' * (total_width - overall_bar_width)
        
        print("\nOverall Progress")
        print(f"{self.theme.apply_color(overall_bar, 'primary')} {overall_progress*100:3.0f}%")
    
    @contextmanager
    def loading(self, message: str, style: str = 'dots') -> Generator:
        """
        Show loading spinner while executing a task
        """
        def show_spinner():
            spinner = self.theme.ICONS.get('loading', ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
            char = spinner[self._spinner_idx % len(spinner)]
            self._spinner_idx += 1
            return char
        
        try:
            # Start loading animation
            print(f"\r{message} {show_spinner()}", end='', flush=True)
            while True:
                time.sleep(0.1)
                print(f"\r{message} {show_spinner()}", end='', flush=True)
                yield
        finally:
            # Clear loading animation
            print("\r" + " " * (len(message) + 2) + "\r", end='', flush=True)
    
    def multi_stage(self, stages: List[Dict]) -> None:
        """
        Show multi-stage progress
        Example:
        System Check
        ├─ ✓ Checking Python...       [done]
        ├─ ✓ Checking yt-dlp...       [done]
        ├─ ⧗ Checking ffmpeg...       [in progress]
        └─   Checking internet...     [waiting]
        """
        for i, stage in enumerate(stages):
            prefix = '└─' if i == len(stages) - 1 else '├─'
            status = stage['status']

            if status == 'completed':
                icon = self.theme.apply_color('✓', 'success')
            elif status == 'error':
                icon = self.theme.apply_color('✗', 'error')
            elif status == 'in_progress':
                icon = self.theme.apply_color('⧗', 'primary')
            else:
                icon = ' '

            line = f"{prefix} {icon} {stage['message']}"

            if status == 'completed':
                line += self.theme.apply_color(' [done]', 'success')
            elif status == 'error':
                line += self.theme.apply_color(f" [{stage.get('error', 'failed')}]", 'error')
            elif status == 'in_progress':
                line += self.theme.apply_color(' [in progress]', 'primary')

            print(line)

    def smooth_download_progress(self, title: str, download_callback: Callable[[RichProgress, TaskID], None]):
        """
        Show smooth download progress with spinner → progress bar transition

        Args:
            title: Description of what's being downloaded
            download_callback: Function that receives (progress, task_id) and performs download

        Example:
            def download(progress, task_id):
                for i in range(100):
                    progress.update(task_id, advance=1)
                    time.sleep(0.1)

            enhanced_progress.smooth_download_progress("Downloading video", download)
        """
        self.live_display.transition_spinner_to_progress(
            f"Preparing {title}...",
            lambda progress: download_callback(progress, progress.add_task(title, total=100))
        )

    @contextmanager
    def live_progress_context(self, preparing_message: str):
        """
        Context manager for smooth progress display with preparation phase

        Args:
            preparing_message: Message to show during preparation

        Yields:
            Rich Progress object

        Example:
            with progress.live_progress_context("Fetching videos") as prog:
                task = prog.add_task("Download", total=100)
                for i in range(100):
                    prog.update(task, advance=1)
        """
        # Show spinner briefly during preparation
        with self.live_display.spinner_context(preparing_message):
            time.sleep(0.2)  # Brief preparation indication

        # Then show progress bar
        with self.live_display.progress_context() as progress:
            yield progress

    def show_video_list_smooth(self, videos: List[Dict], delay: float = 0.03):
        """
        Display video list with smooth scroll-in effect

        Args:
            videos: List of video dicts with 'title', 'duration', etc.
            delay: Delay between each line
        """
        lines = []
        for i, video in enumerate(videos, 1):
            duration = video.get('duration', 0)
            minutes = duration // 60
            seconds = duration % 60

            lines.append(f"[cyan]{i:3d}.[/cyan] {video['title']}")
            lines.append(f"     [dim]Duration: {minutes}:{seconds:02d}[/dim]")

        self.live_display.scroll_in_content(lines, delay=delay)