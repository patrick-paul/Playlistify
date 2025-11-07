"""
Main CLI interface
"""
import sys
import time
from typing import Dict, Optional
from pathlib import Path

from .ui.theme import Theme
from .ui.components import Box, Progress, Status
from .ui.interactive import Prompt
from .ui.live_display import LiveDisplay
from .core.downloader import DownloadEngine
from .utils.errors import DownloadError, ErrorHandler
from .services.dependencies import DependencyManager
from .config.settings import Config

class CLI:
    """Main CLI application interface"""

    def __init__(self):
        self.theme = Theme()
        self.live_display = LiveDisplay(self.theme)
        self.box = Box(self.theme)
        self.progress = Progress(self.theme)
        self.status = Status(self.theme)
        self.prompt = Prompt(self.theme)
        self.downloader = DownloadEngine(self.theme, self.live_display)
        self.error_handler = ErrorHandler(self.theme)
        self.dependency_manager = DependencyManager(self.theme)
        self.config = Config.load()

        # Session tracking
        self.session_downloads = []
        self.session_failed = []

        # Setup callbacks - DISABLED: Rich Live display handles progress natively
        # The old callback system conflicts with Rich's transient progress bars
        # self.downloader.on_progress(self._handle_progress)
        # self.downloader.on_complete(self._handle_complete)
    
    def run(self):
        """Main application loop"""
        try:
            self._show_welcome()

            # Check dependencies first
            if not self.dependency_manager.check_all():
                print(f"\n{self.status.error('Dependency check failed')}")
                print("Please resolve the issues above before continuing.")
                return

            while True:
                choice = self._show_main_menu()

                if choice == 0:  # Download single video
                    self._handle_single_video()
                elif choice == 1:  # Download playlist
                    self._handle_playlist()
                elif choice == 2:  # Show settings
                    self._handle_settings()
                elif choice == 3:  # Exit
                    self._show_goodbye()
                    break

                # Show stats after each operation
                self._show_session_stats()

        except KeyboardInterrupt:
            print(f"\n{self.status.info('Operation cancelled by user')}")
            sys.exit(0)
    
    def _show_welcome(self):
        """Display welcome screen"""
        print("\n" + self.box.header(
            "YouTube Playlist Downloader",
            "Fast • Reliable • Beautiful"
        ))
        print()
    
    def _show_main_menu(self) -> int:
        """Show main menu and get user choice"""
        options = [
            "Download single video",
            "Download playlist",
            "Settings",
            "Exit"
        ]
        
        print(self.box.section("Main Menu"))
        return self.prompt.select("What would you like to do?", options)
    
    def _handle_single_video(self):
        """Handle single video download workflow"""
        print(self.box.section("Single Video Download"))

        # Get video URL with validation
        url = self.prompt.input(
            "Enter YouTube video URL",
            validator=lambda x: x.strip() and ('youtube.com' in x or 'youtu.be' in x)
        )
        if not url:
            print(self.status.error("No URL provided"))
            return

        # Get quality preference (ask only if not set as default)
        if self.config.ask_quality:
            quality_options = [
                "Best available",
                "1080p",
                "720p",
                "480p",
                "Lowest (fastest)"
            ]
            quality_map = ['best', '1080p', '720p', '480p', 'worst']
            quality_choice = self.prompt.select("Select quality", quality_options)
            quality = quality_map[quality_choice]

            # Ask if user wants to save as default
            if self.prompt.confirm("Save as default quality and don't ask again?", default=False):
                self.config.set_default('quality', quality, dont_ask_again=True)
                self.config.save()
                print(self.status.success(f"Default quality set to: {quality}"))
        else:
            quality = self.config.quality
            print(self.status.info(f"Using default quality: {quality}"))

        # Get output directory (ask only if not set as default)
        if self.config.ask_download_dir:
            output_dir = self.prompt.input(
                "Enter output directory",
                default=self.config.output_dir
            )

            # Ask if user wants to save as default
            if output_dir != self.config.output_dir:
                if self.prompt.confirm("Save as default download directory and don't ask again?", default=False):
                    self.config.set_default('output_dir', output_dir, dont_ask_again=True)
                    self.config.save()
                    print(self.status.success(f"Default directory set to: {output_dir}"))
        else:
            output_dir = self.config.output_dir
            print(self.status.info(f"Using default directory: {output_dir}"))

        Path(output_dir).mkdir(parents=True, exist_ok=True)

        # Start download
        try:
            print(self.box.section("Downloading"))
            self.downloader.download_single_video(
                {'url': url, 'title': 'Video'},
                output_dir,
                quality
            )
        except DownloadError as e:
            print("\n" + self.error_handler.format_error(e))
    
    def _handle_playlist(self):
        """Handle playlist download workflow"""
        print(self.box.section("Playlist Download"))

        # Get playlist URL with validation
        url = self.prompt.input(
            "Enter YouTube playlist URL",
            validator=lambda x: x.strip() and ('youtube.com' in x or 'youtu.be' in x) and ('list=' in x or 'playlist' in x.lower())
        )
        if not url:
            print(self.status.error("No URL provided or invalid playlist URL"))
            return

        try:
            # Fetch playlist info
            info = self.downloader.get_playlist_info(url)
            if not info:
                print(self.status.error("Failed to fetch playlist information"))
                return
                
            print("\nPlaylist Information:")
            print(f"{self.theme.style('Title:', 'info')} {info['title']}")
            print(f"{self.theme.style('Videos:', 'info')} {len(info['videos'])}")
            print(f"{self.theme.style('Creator:', 'info')} {info.get('creator', 'Unknown')}\n")
            
            # Get download options
            options = [
                "Download entire playlist",
                "Select video range",
                "Choose specific videos",
                "List videos only (no download)"
            ]
            choice = self.prompt.select("What would you like to do?", options)
            
            if choice == 0:  # Full playlist
                self._download_full_playlist(info)
            elif choice == 1:  # Range
                self._download_video_range(info)
            elif choice == 2:  # Specific videos
                self._download_specific_videos(info)
            elif choice == 3:  # List only
                self._list_playlist_videos(info)
                
        except Exception as e:
            print("\n" + self.error_handler.format_error(e))
    
    def _handle_settings(self):
        """Handle settings menu"""
        while True:
            print(self.box.section("Settings"))

            # Display current settings
            print("\nCurrent Settings:")
            print(f"  {self.theme.apply_color('Video Quality:', 'info')} {self.config.quality}")
            print(f"  {self.theme.apply_color('Download Directory:', 'info')} {self.config.output_dir}")
            print(f"  {self.theme.apply_color('Download Mode:', 'info')} {'Parallel' if self.config.use_parallel else 'Sequential'}")
            print(f"  {self.theme.apply_color('Parallel Workers:', 'info')} {self.config.parallel_workers}")
            print(f"  {self.theme.apply_color('Max Retries:', 'info')} {self.config.max_retries}")
            print()
            print("Prompt Settings:")
            print(f"  {self.theme.apply_color('Ask for quality:', 'muted')} {'Yes' if self.config.ask_quality else 'No (using default)'}")
            print(f"  {self.theme.apply_color('Ask for directory:', 'muted')} {'Yes' if self.config.ask_download_dir else 'No (using default)'}")
            print(f"  {self.theme.apply_color('Ask for parallel mode:', 'muted')} {'Yes' if self.config.ask_parallel_mode else 'No (using default)'}")
            print(f"  {self.theme.apply_color('Ask for num workers:', 'muted')} {'Yes' if self.config.ask_num_workers else 'No (using default)'}")

            options = [
                "Change video quality",
                "Change download directory",
                "Change download mode (parallel/sequential)",
                "Change number of parallel workers",
                "Change max retries",
                "Re-enable all prompts",
                "Reset all settings to defaults",
                "Back to main menu"
            ]

            choice = self.prompt.select("What would you like to do?", options)

            if choice == 0:  # Change quality
                quality_options = [
                    "Best available",
                    "1080p",
                    "720p",
                    "480p",
                    "Lowest (fastest)"
                ]
                quality_map = ['best', '1080p', '720p', '480p', 'worst']
                quality_choice = self.prompt.select("Select quality", quality_options)
                quality = quality_map[quality_choice]
                self.config.quality = quality
                self.config.save()
                print(self.status.success(f"Quality set to: {quality}"))

            elif choice == 1:  # Change directory
                output_dir = self.prompt.input(
                    "Enter new download directory",
                    default=self.config.output_dir
                )
                self.config.output_dir = output_dir
                self.config.save()
                print(self.status.success(f"Download directory set to: {output_dir}"))

            elif choice == 2:  # Change download mode
                use_parallel = self.prompt.confirm(
                    "Use parallel downloads?",
                    default=self.config.use_parallel
                )
                self.config.use_parallel = use_parallel
                self.config.save()
                print(self.status.success(f"Download mode set to: {'parallel' if use_parallel else 'sequential'}"))

            elif choice == 3:  # Change number of workers
                max_workers = self.prompt.input(
                    "Number of parallel downloads (1-10)",
                    default=str(self.config.parallel_workers),
                    validator=lambda x: x.isdigit() and 1 <= int(x) <= 10
                )
                self.config.parallel_workers = int(max_workers)
                self.config.save()
                print(self.status.success(f"Parallel workers set to: {max_workers}"))

            elif choice == 4:  # Change max retries
                max_retries = self.prompt.input(
                    "Maximum number of retries (1-10)",
                    default=str(self.config.max_retries),
                    validator=lambda x: x.isdigit() and 1 <= int(x) <= 10
                )
                self.config.max_retries = int(max_retries)
                self.config.save()
                print(self.status.success(f"Max retries set to: {max_retries}"))

            elif choice == 5:  # Re-enable all prompts
                self.config.ask_quality = True
                self.config.ask_download_dir = True
                self.config.ask_parallel_mode = True
                self.config.ask_num_workers = True
                self.config.save()
                print(self.status.success("All prompts re-enabled!"))

            elif choice == 6:  # Reset all settings
                if self.prompt.confirm("Are you sure you want to reset all settings to defaults?", default=False):
                    self.config.reset_to_defaults()
                    self.config.save()
                    print(self.status.success("All settings reset to defaults!"))

            elif choice == 7:  # Back to main menu
                break

            print()  # Add spacing
    
    def _show_goodbye(self):
        """Show exit message"""
        print("\n" + self.box.header("Thank you for using YouTube Downloader"))
        print()
    
    def _show_session_stats(self):
        """Show download statistics with smooth presentation"""
        if self.session_downloads or self.session_failed:
            self.live_display.print()
            self.live_display.print("[bold cyan]Session Statistics[/bold cyan]")
            self.live_display.print(f"  [dim]Total Downloads:[/dim] {len(self.session_downloads)}")
            self.live_display.print(f"  [green]Successful:[/green] {len([d for d in self.session_downloads if d.get('success')])}")
            self.live_display.print(f"  [red]Failed:[/red] {len(self.session_failed)}")
            self.live_display.print()
        
    def _download_full_playlist(self, info):
        """Download entire playlist"""
        # Get quality preference (ask only if not set as default)
        if self.config.ask_quality:
            quality_options = [
                "Best available",
                "1080p",
                "720p",
                "480p",
                "Lowest (fastest)"
            ]
            quality_map = ['best', '1080p', '720p', '480p', 'worst']
            quality_choice = self.prompt.select("Select quality", quality_options)
            quality = quality_map[quality_choice]

            # Ask if user wants to save as default
            if self.prompt.confirm("Save as default quality and don't ask again?", default=False):
                self.config.set_default('quality', quality, dont_ask_again=True)
                self.config.save()
                print(self.status.success(f"Default quality set to: {quality}"))
        else:
            quality = self.config.quality
            print(self.status.info(f"Using default quality: {quality}"))

        # Get output directory (ask only if not set as default)
        if self.config.ask_download_dir:
            output_dir = self.prompt.input(
                "Enter output directory",
                default=self.config.output_dir
            )

            # Ask if user wants to save as default
            if output_dir != self.config.output_dir:
                if self.prompt.confirm("Save as default download directory and don't ask again?", default=False):
                    self.config.set_default('output_dir', output_dir, dont_ask_again=True)
                    self.config.save()
                    print(self.status.success(f"Default directory set to: {output_dir}"))
        else:
            output_dir = self.config.output_dir
            print(self.status.info(f"Using default directory: {output_dir}"))

        Path(output_dir).mkdir(parents=True, exist_ok=True)

        # Get parallel download preference (ask only if not set as default)
        if self.config.ask_parallel_mode:
            use_parallel = self.prompt.confirm(
                "Use parallel downloads? (faster but less stable)",
                default=self.config.use_parallel
            )

            # Ask if user wants to save as default
            if self.prompt.confirm("Save as default download mode and don't ask again?", default=False):
                self.config.set_default('use_parallel', use_parallel, dont_ask_again=True)
                self.config.save()
                print(self.status.success(f"Default mode set to: {'parallel' if use_parallel else 'sequential'}"))
        else:
            use_parallel = self.config.use_parallel
            print(self.status.info(f"Using default mode: {'parallel' if use_parallel else 'sequential'}"))

        if use_parallel:
            # Get number of workers (ask only if not set as default)
            if self.config.ask_num_workers:
                max_workers = self.prompt.input(
                    "Number of parallel downloads (1-5)",
                    default=str(self.config.parallel_workers),
                    validator=lambda x: x.isdigit() and 1 <= int(x) <= 5
                )
                max_workers = int(max_workers)

                # Ask if user wants to save as default
                if max_workers != self.config.parallel_workers:
                    if self.prompt.confirm("Save as default number of workers and don't ask again?", default=False):
                        self.config.set_default('parallel_workers', max_workers, dont_ask_again=True)
                        self.config.save()
                        print(self.status.success(f"Default workers set to: {max_workers}"))
            else:
                max_workers = self.config.parallel_workers
                print(self.status.info(f"Using default workers: {max_workers}"))
        else:
            max_workers = 1

        # Start download
        try:
            print(self.box.section("Downloading Playlist"))
            self.downloader.download_playlist(
                info,
                output_dir=output_dir,
                quality=quality,
                max_workers=max_workers
            )
        except Exception as e:
            print("\n" + self.error_handler.format_error(e))
            
    def _download_video_range(self, info):
        """Download a range of videos from the playlist"""
        total_videos = len(info['videos'])
        
        # Get range
        while True:
            range_input = self.prompt.input(
                f"Enter video range (1-{total_videos}, e.g. 1-10)",
                validator=lambda x: '-' in x and 
                                  all(p.isdigit() for p in x.split('-')) and
                                  1 <= int(x.split('-')[0]) <= total_videos and
                                  1 <= int(x.split('-')[1]) <= total_videos
            )
            
            start, end = map(int, range_input.split('-'))
            if start <= end:
                break
            print(self.status.error("Start must be less than or equal to end"))
            
        # Update video list
        info['videos'] = info['videos'][start-1:end]
        
        # Download selected range
        self._download_full_playlist(info)
        
    def _download_specific_videos(self, info):
        """Let user choose specific videos to download"""
        # Create video selection menu (just show titles without numbering since multi_select adds them)
        options = [v['title'] for v in info['videos']]
        selected = self.prompt.multi_select(
            "Select videos to download",
            options
        )

        if not selected:
            print(self.status.warning("No videos selected"))
            return

        # Update video list with selections
        info['videos'] = [info['videos'][i] for i in selected]

        # Download selected videos
        self._download_full_playlist(info)
        
    def _list_playlist_videos(self, info):
        """Display playlist video information with smooth scroll-in effect"""
        self.live_display.print_section_header("Playlist Videos")

        # Build list of lines to display
        lines = []
        for i, video in enumerate(info['videos'], 1):
            duration = video.get('duration', 0)
            minutes = duration // 60
            seconds = duration % 60

            lines.append(f"[cyan bold]{i:3d}.[/cyan bold] {video['title']}")
            lines.append(f"     [blue]Duration:[/blue] {minutes}:{seconds:02d}")
            lines.append("")  # Spacing

        # Display with smooth scroll-in effect
        self.live_display.scroll_in_content(lines, delay=0.02)
    
    def _handle_progress(self, info: Dict):
        """Handle progress updates"""
        if info['status'] == 'downloading' and 'progress' in info:
            print(self.progress.bar(
                int(info['progress']),
                100,
                prefix=f"Downloading {info['video'].get('title', 'Video')}"
            ), end='\r')
    
    def _handle_complete(self, info: Dict):
        """Handle download completion"""
        if info['status'] == 'success':
            print("\n" + self.status.success(
                f"Downloaded {info['video'].get('title', 'Video')}"
            ))

def main():
    """Application entry point"""
    cli = CLI()
    cli.run()

if __name__ == "__main__":
    main()