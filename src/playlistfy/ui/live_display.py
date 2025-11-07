"""
Live display manager for smooth, controlled UI updates with Rich
"""
import sys
import time
from typing import Optional, List, Dict, Any, Callable
from contextlib import contextmanager
from rich.console import Console, Group
from rich.live import Live
from rich.spinner import Spinner
from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    TextColumn,
    DownloadColumn,
    TransferSpeedColumn,
    TimeRemainingColumn,
    TaskID,
)
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.text import Text
from .theme import Theme


# Choose safe spinner for Windows that doesn't use Unicode
SAFE_SPINNER = "line" if sys.platform == "win32" else "dots"


class LiveDisplay:
    """
    Manages smooth, controlled UI updates using Rich Live rendering

    Features:
    - Smooth transitions between UI states (spinner → progress bar)
    - Live updating regions that don't spam the terminal
    - Controlled content reveals with optional scroll-in effects
    - Dedicated log/output areas
    - Professional, flicker-free updates
    """

    def __init__(self, theme: Theme):
        self.theme = theme
        # Force UTF-8 encoding for Windows console to support Rich features
        self.console = Console(force_terminal=True, legacy_windows=False)
        self._live_context: Optional[Live] = None
        self._current_display: Optional[Any] = None

    @contextmanager
    def spinner_context(self, message: str, style: str = "cyan"):
        """
        Show a spinner that updates smoothly in place

        Args:
            message: The message to display next to the spinner
            style: Color style for the spinner

        Example:
            with live_display.spinner_context("Fetching playlist..."):
                # Long running operation
                playlist_data = fetch_playlist()
        """
        spinner = Spinner(SAFE_SPINNER, text=message, style=style)

        with Live(spinner, console=self.console, refresh_per_second=10, transient=True) as live:
            self._live_context = live
            try:
                yield live
            finally:
                self._live_context = None

    @contextmanager
    def progress_context(self, description: str = "Processing..."):
        """
        Create a smooth progress bar context with multiple tasks support

        Args:
            description: Default description for the progress display

        Returns:
            Rich Progress object for adding tasks

        Example:
            with live_display.progress_context("Downloading videos") as progress:
                task = progress.add_task("Video 1", total=100)
                for i in range(100):
                    progress.update(task, advance=1)
        """
        progress = Progress(
            TextColumn("[bold white]{task.description}"),
            BarColumn(
                complete_style="bold cyan",
                finished_style="bold cyan",
                bar_width=40
            ),
            TextColumn("[bold white]{task.percentage:>3.0f}%"),
            TextColumn("[bold white]({task.completed}/{task.total})"),
            console=self.console,
            expand=False
        )

        # Use transient=True to auto-clear the progress bar when done
        # Increase refresh rate for smoother updates
        with Live(progress, console=self.console, refresh_per_second=20, transient=True) as live:
            self._live_context = live
            try:
                yield progress
            finally:
                self._live_context = None
                # Small delay to ensure clean clearing on Windows
                time.sleep(0.05)

    @contextmanager
    def panel_context(self, title: str, border_style: str = "cyan"):
        """
        Create a live-updating panel for displaying structured content

        Args:
            title: Panel title
            border_style: Border color style

        Yields:
            A function to update the panel content

        Example:
            with live_display.panel_context("Status") as update:
                update("Processing file 1...")
                time.sleep(1)
                update("Processing file 2...")
        """
        content = Text("")
        panel = Panel(content, title=title, border_style=border_style)

        with Live(panel, console=self.console, refresh_per_second=4) as live:
            def update_content(new_content: str, style: str = "white"):
                content.plain = new_content
                content.style = style
                live.update(Panel(content, title=title, border_style=border_style))

            self._live_context = live
            try:
                yield update_content
            finally:
                self._live_context = None

    @contextmanager
    def multi_section_context(self):
        """
        Create a live display with multiple sections (logs, progress, status)

        This prevents the UI from jumping around as new content arrives.
        Each section updates independently.

        Example:
            with live_display.multi_section_context() as sections:
                sections.update_status("Starting download...")
                sections.add_log("Connecting to server")
                sections.update_progress(50)
        """
        layout = Layout()
        layout.split_column(
            Layout(name="status", size=3),
            Layout(name="progress", size=5),
            Layout(name="logs", size=10)
        )

        # Initialize sections
        status_text = Text("Ready", style="green")
        progress_display = Text("No active tasks")
        logs_display = Text("")

        layout["status"].update(Panel(status_text, title="Status", border_style="green"))
        layout["progress"].update(Panel(progress_display, title="Progress", border_style="cyan"))
        layout["logs"].update(Panel(logs_display, title="Logs", border_style="blue"))

        logs_buffer = []

        class MultiSectionController:
            def update_status(self, message: str, style: str = "green"):
                status_text.plain = message
                status_text.style = style
                layout["status"].update(Panel(status_text, title="Status", border_style=style))

            def update_progress(self, message: str):
                progress_display.plain = message
                layout["progress"].update(Panel(progress_display, title="Progress", border_style="cyan"))

            def add_log(self, message: str, max_logs: int = 20):
                logs_buffer.append(message)
                if len(logs_buffer) > max_logs:
                    logs_buffer.pop(0)
                logs_display.plain = "\n".join(logs_buffer)
                layout["logs"].update(Panel(logs_display, title="Logs", border_style="blue"))

        controller = MultiSectionController()

        with Live(layout, console=self.console, refresh_per_second=4) as live:
            self._live_context = live
            try:
                yield controller
            finally:
                self._live_context = None

    def transition_spinner_to_progress(self, spinner_message: str,
                                      progress_callback: Callable[[Progress], None]):
        """
        Smoothly transition from a spinner to a progress bar

        This is the key method for preventing abrupt UI changes.

        Args:
            spinner_message: Message to show with spinner
            progress_callback: Function that receives Progress object and performs the task

        Example:
            def download_task(progress):
                task = progress.add_task("Downloading", total=100)
                for i in range(100):
                    progress.update(task, advance=1)
                    time.sleep(0.1)

            display.transition_spinner_to_progress(
                "Preparing download...",
                download_task
            )
        """
        # Phase 1: Show spinner while preparing
        with self.spinner_context(spinner_message):
            time.sleep(0.3)  # Brief pause to show spinner

        # Phase 2: Clear and show progress bar
        with self.progress_context() as progress:
            progress_callback(progress)

    def scroll_in_content(self, lines: List[str], delay: float = 0.05):
        """
        Display content with a controlled "scroll-in" effect

        Args:
            lines: List of lines to display
            delay: Delay between each line (seconds)

        This creates a sense of motion without being too slow or spammy.
        """
        for line in lines:
            self.console.print(line)
            if delay > 0:
                time.sleep(delay)

    def print_transition(self, old_message: str, new_message: str,
                        pause_duration: float = 0.2):
        """
        Print a message, pause, then replace it with a new message

        Creates a clear visual transition between states.

        Args:
            old_message: Initial message
            new_message: Message to replace it with
            pause_duration: How long to show the old message
        """
        self.console.print(old_message)
        time.sleep(pause_duration)
        self.console.print(new_message)

    def clear_lines(self, num_lines: int = 1):
        """
        Clear a specific number of lines from the terminal

        Useful for replacing content without stacking.
        """
        for _ in range(num_lines):
            self.console.print("\033[A\033[K", end="")

    def print_section_header(self, title: str, style: str = "bold cyan"):
        """
        Print a section header with proper spacing and styling
        """
        # Use safe ASCII characters on Windows
        separator = '-' * 40 if sys.platform == "win32" else '─' * 40

        self.console.print()
        self.console.print(f"[{style}]{separator}[/{style}]")
        self.console.print(f"[{style}]{title}[/{style}]")
        self.console.print(f"[{style}]{separator}[/{style}]")
        self.console.print()

    def show_completion_summary(self, title: str, items: List[Dict[str, Any]]):
        """
        Show a summary table after completing operations

        Args:
            title: Title for the summary
            items: List of dicts with 'name', 'status', 'details' keys
        """
        table = Table(title=title, show_header=True, header_style="bold cyan")
        table.add_column("Item", style="white")
        table.add_column("Status", justify="center")
        table.add_column("Details", style="dim")

        # Use safe icons on Windows
        if sys.platform == "win32":
            success_icon = "[OK]"
            error_icon = "[X]"
        else:
            success_icon = "✓"
            error_icon = "✗"

        for item in items:
            status_icon = success_icon if item.get("status") == "success" else error_icon
            status_style = "green" if item.get("status") == "success" else "red"

            table.add_row(
                item.get("name", "Unknown"),
                f"[{status_style}]{status_icon}[/{status_style}]",
                item.get("details", "")
            )

        self.console.print(table)

    def print(self, *args, **kwargs):
        """
        Wrapper around console.print for consistent output
        """
        self.console.print(*args, **kwargs)

    def print_status(self, message: str, status: str = "info"):
        """
        Print a status message with appropriate styling

        Args:
            message: The message to display
            status: One of 'success', 'error', 'warning', 'info'
        """
        style_map = {
            "success": "green",
            "error": "red",
            "warning": "yellow",
            "info": "cyan"
        }

        # Use safe ASCII icons on Windows
        if sys.platform == "win32":
            icon_map = {
                "success": "[OK]",
                "error": "[X]",
                "warning": "[!]",
                "info": "[i]"
            }
        else:
            icon_map = {
                "success": "✓",
                "error": "✗",
                "warning": "⚠",
                "info": "ℹ"
            }

        style = style_map.get(status, "white")
        icon = icon_map.get(status, "•")

        self.console.print(f"[{style}]{icon}[/{style}] {message}")
