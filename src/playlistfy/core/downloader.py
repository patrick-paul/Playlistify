"""
Core download engine
"""
import os
import sys
import time
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Callable
from rich.progress import Progress as RichProgress, TaskID
from ..utils.errors import DownloadError, ErrorHandler
from ..ui.theme import Theme
from ..ui.components import Progress, Status
from ..ui.live_display import LiveDisplay

class DownloadEngine:
    """Core download functionality with smooth progress tracking"""

    def __init__(self, theme: Theme, live_display: Optional[LiveDisplay] = None):
        self.theme = theme
        self.live_display = live_display or LiveDisplay(theme)
        self.progress = Progress(theme)
        self.status = Status(theme)
        self.error_handler = ErrorHandler(theme)
        self._progress_callback = None
        self._complete_callback = None
    
    def on_progress(self, callback: Callable[[Dict], None]) -> None:
        """Register progress callback"""
        self._progress_callback = callback
    
    def on_complete(self, callback: Callable[[Dict], None]) -> None:
        """Register completion callback"""
        self._complete_callback = callback
    
    def _emit_progress(self, info: Dict) -> None:
        """Emit progress update"""
        if self._progress_callback:
            self._progress_callback(info)
    
    def _emit_complete(self, info: Dict) -> None:
        """Emit completion update"""
        if self._complete_callback:
            self._complete_callback(info)
    
    def download_single_video(self, video: Dict, output_dir: str, quality: str,
                            max_retries: int = 3, use_cookies: Optional[str] = None) -> bool:
        """
        Download a single video with smooth progress tracking and transitions
        """
        try:
            # Ensure output directory exists
            Path(output_dir).mkdir(parents=True, exist_ok=True)

            video_title = video.get('title', 'Video')

            # Phase 1: Smooth spinner while fetching info and verifying quality
            with self.live_display.spinner_context(f"Fetching {video_title}..."):
                # Check available formats and determine best quality
                available_quality = self._verify_and_get_quality(
                    video['url'],
                    quality,
                    use_cookies
                )

                # Notify user if quality was adjusted
                if available_quality != quality:
                    self.live_display.print_status(
                        f"Quality adjusted: {quality} → {available_quality}",
                        status="warning"
                    )

                # Prepare command with verified quality
                cmd = self._build_ytdlp_command(
                    video['url'],
                    output_dir=output_dir,
                    quality=available_quality,
                    use_cookies=use_cookies
                )
                time.sleep(0.3)  # Brief pause to show spinner

            # Phase 2: Smooth transition to progress bar
            with self.live_display.progress_context(f"Downloading {video_title}") as progress:
                task = progress.add_task(video_title, total=100)

                # Start download with progress tracking
                self._emit_progress({
                    'status': 'starting',
                    'video': video
                })

                # Execute download with completely suppressed output
                import threading

                # Use PIPE for both stdout and stderr, then discard them
                # This prevents any output from leaking to the terminal
                kwargs = {
                    'stdout': subprocess.PIPE,
                    'stderr': subprocess.PIPE,
                    'text': True
                }

                # Suppress console window on Windows
                if sys.platform == "win32":
                    # CREATE_NO_WINDOW flag (0x08000000) prevents console window
                    kwargs['creationflags'] = 0x08000000

                process = subprocess.Popen(cmd, **kwargs)

                def animate_progress():
                    """Animate progress bar while download is running"""
                    completed = 0
                    while process.poll() is None and completed < 95:
                        # Increment progress gradually
                        time.sleep(0.1)
                        completed = min(completed + 2, 95)
                        progress.update(task, completed=completed)

                        self._emit_progress({
                            'status': 'downloading',
                            'video': video,
                            'progress': completed
                        })

                # Start animation thread
                animation_thread = threading.Thread(target=animate_progress, daemon=True)
                animation_thread.start()

                # Wait for download to complete
                process.wait()
                animation_thread.join(timeout=1)

                # Check for errors
                if process.returncode != 0:
                    stderr_output = process.stderr.read() if process.stderr else ""
                    raise DownloadError(f"Download failed: {stderr_output}")

                # Ensure progress bar reaches 100% before clearing
                progress.update(task, completed=100)
                time.sleep(0.2)  # Brief pause to show 100% completion

                # Consume any remaining output to prevent leaks
                if process.stdout:
                    process.stdout.read()
                if process.stderr:
                    process.stderr.read()

            # Phase 3: Success message after progress bar is cleared
            # Add small delay to ensure clean transition
            time.sleep(0.1)
            if process.returncode == 0:
                self.live_display.print_status(
                    f"Downloaded: {video_title}",
                    status="success"
                )
                self._emit_complete({
                    'status': 'success',
                    'video': video
                })
                return True

            raise DownloadError(f"Download failed with code {process.returncode}")

        except Exception as e:
            error = self.error_handler.analyze_error(e)
            error.video = video
            self.live_display.print_status(
                f"Failed to download: {video.get('title', 'Video')}",
                status="error"
            )
            self._emit_progress({
                'status': 'error',
                'video': video,
                'error': error
            })
            raise error
    
    def _verify_and_get_quality(self, url: str, requested_quality: str,
                                use_cookies: Optional[str] = None) -> str:
        """
        Verify available formats and determine the best quality to use.
        Implements progressive fallback: 1080p -> 720p -> 480p -> best
        """
        try:
            # Get available formats
            cmd = ['yt-dlp', '--list-formats', '--no-warnings']

            # Add cookie handling
            if use_cookies:
                cmd.extend(['--cookies-from-browser', use_cookies])
            else:
                cmd.extend([
                    '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    '--extractor-args', 'youtube:player_client=android,web',
                    '--no-check-certificate',
                ])

            cmd.append(url)

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            formats_output = result.stdout.lower()

            # Define quality hierarchy for fallback
            quality_hierarchy = {
                '1080p': ['1080', '720', '480', 'best'],
                '720p': ['720', '480', 'best'],
                '480p': ['480', 'best'],
                'best': ['best'],
                'worst': ['worst']
            }

            # Get fallback chain for requested quality
            fallback_chain = quality_hierarchy.get(requested_quality, ['best'])

            # Check which qualities are available
            for quality_option in fallback_chain:
                if quality_option == 'best' or quality_option == 'worst':
                    # Always available
                    return quality_option

                # Check if this quality is available in the formats
                if f'{quality_option}p' in formats_output or f'{quality_option}x' in formats_output:
                    # Log the fallback if different from requested
                    if quality_option != requested_quality.replace('p', ''):
                        print(self.status.warning(
                            f"Requested quality {requested_quality} not available, using {quality_option}p"
                        ))
                    return f'{quality_option}p'

            # If no specific quality found, default to best
            if requested_quality != 'best':
                print(self.status.warning(
                    f"Requested quality {requested_quality} not available, using best available"
                ))
            return 'best'

        except subprocess.TimeoutExpired:
            # If format check times out, use requested quality and let yt-dlp handle it
            print(self.status.warning(
                f"Quality verification timed out, attempting {requested_quality}"
            ))
            return requested_quality
        except Exception as e:
            # If format check fails, use requested quality and let yt-dlp handle it
            print(self.status.warning(
                f"Could not verify quality: {str(e)}, attempting {requested_quality}"
            ))
            return requested_quality

    def _build_ytdlp_command(self, url: str, output_dir: str, quality: str,
                            use_cookies: Optional[str] = None) -> List[str]:
        """Build yt-dlp command with all options"""
        # Improved quality formats with progressive fallback
        quality_formats = {
            'best': 'bestvideo+bestaudio/best',
            '1080p': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]/bestvideo[height<=720]+bestaudio/best[height<=720]',
            '720p': 'bestvideo[height<=720]+bestaudio/best[height<=720]/bestvideo[height<=480]+bestaudio/best[height<=480]',
            '480p': 'bestvideo[height<=480]+bestaudio/best[height<=480]/worst',
            'worst': 'worstvideo+worstaudio/worst'
        }

        format_string = quality_formats.get(quality, quality_formats['best'])
        
        cmd = [
            'yt-dlp',
            '-f', format_string,
            '--merge-output-format', 'mp4',
            '-o', f'{output_dir}/%(title)s.%(ext)s',
            '--quiet',  # Suppress ALL output
            '--no-warnings'  # Suppress warnings too
        ]
        
        # Add cookie handling
        if use_cookies:
            cmd.extend(['--cookies-from-browser', use_cookies])
        else:
            cmd.extend([
                '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                '--extractor-args', 'youtube:player_client=android,web',
                '--no-check-certificate',
            ])
        
        cmd.append(url)
        return cmd
    
    def _parse_progress(self, line: str) -> Optional[Dict]:
        """Parse progress information from yt-dlp output"""
        if '[download]' not in line:
            return None

        try:
            # Extract percentage from yt-dlp output (e.g., "[download] 45.2% of...")
            if '%' in line:
                # Find the percentage value
                parts = line.split('%')
                if len(parts) >= 2:
                    # Get the last number before the % sign
                    before_percent = parts[0].strip().split()[-1]
                    percent = float(before_percent)
                    return {
                        'progress': min(percent, 100),
                        'raw_line': line
                    }
        except:
            pass

        return None
        
    def get_playlist_info(self, url: str) -> Optional[Dict]:
        """Extract playlist information and video URLs with smooth spinner"""
        try:
            # Smooth spinner while fetching playlist info
            with self.live_display.spinner_context("Fetching playlist info..."):
                # Get playlist info using yt-dlp
                cmd = [
                    'yt-dlp',
                    '--flat-playlist',
                    '--dump-json',
                    url
                ]

                result = subprocess.run(cmd, capture_output=True, text=True, check=True)

            # Process results after spinner clears
            videos = []
            playlist_info = {
                'title': 'Unknown Playlist',
                'creator': 'Unknown',
                'videos': []
            }

            for line in result.stdout.strip().split('\n'):
                if line:
                    try:
                        video_data = json.loads(line)
                        videos.append({
                            'title': video_data.get('title', 'Unknown'),
                            'url': f"https://www.youtube.com/watch?v={video_data['id']}",
                            'id': video_data['id'],
                            'duration': video_data.get('duration', 0)
                        })

                        # Get playlist info from first video
                        if len(videos) == 1:
                            playlist_info['title'] = video_data.get('playlist_title', 'Unknown Playlist')
                            playlist_info['creator'] = video_data.get('uploader', 'Unknown')

                    except json.JSONDecodeError:
                        continue

            playlist_info['videos'] = videos

            # Show success message smoothly
            self.live_display.print_status(
                f"Found {len(videos)} videos in playlist",
                status="success"
            )

            return playlist_info

        except subprocess.CalledProcessError as e:
            error_msg = e.stderr if e.stderr else str(e)
            if 'network' in error_msg.lower() or 'connection' in error_msg.lower():
                raise DownloadError("Network error: Please check your internet connection")
            elif 'private' in error_msg.lower() or 'unavailable' in error_msg.lower():
                raise DownloadError("Playlist is private or unavailable")
            else:
                raise DownloadError(f"Error fetching playlist info: {error_msg}")
        except Exception as e:
            if 'network' in str(e).lower() or 'connection' in str(e).lower():
                raise DownloadError("Network error: Please check your internet connection")
            else:
                raise DownloadError(f"Error fetching playlist info: {str(e)}")
            
    def download_playlist(self, playlist_info: Dict, output_dir: str, quality: str,
                         max_workers: int = 3) -> None:
        """Download all videos in a playlist"""
        from concurrent.futures import ThreadPoolExecutor, as_completed
        import re

        # Create playlist-named folder inside output directory
        playlist_title = playlist_info.get('title', 'Unknown Playlist')
        # Sanitize playlist title for folder name
        safe_playlist_name = re.sub(r'[<>:"/\\|?*]', '_', playlist_title)
        playlist_folder = Path(output_dir) / safe_playlist_name
        playlist_folder.mkdir(parents=True, exist_ok=True)

        videos = playlist_info['videos']

        if not videos:
            raise DownloadError("No videos found in playlist")

        # Add index to video info
        for i, video in enumerate(videos, 1):
            video['index'] = str(i).zfill(3)

        print(self.status.info(f"Starting download of {len(videos)} videos"))
        print(self.status.info(f"Saving to: {playlist_folder}"))

        if max_workers > 1:
            # Parallel download
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = []
                for video in videos:
                    future = executor.submit(
                        self.download_single_video,
                        video=video,
                        output_dir=str(playlist_folder),
                        quality=quality
                    )
                    futures.append(future)

                for future in as_completed(futures):
                    try:
                        future.result()
                    except Exception as e:
                        print("\n" + self.error_handler.format_error(e))

        else:
            # Sequential download
            for video in videos:
                try:
                    self.download_single_video(video, str(playlist_folder), quality)
                except Exception as e:
                    print("\n" + self.error_handler.format_error(e))