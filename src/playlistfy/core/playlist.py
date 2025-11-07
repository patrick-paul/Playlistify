"""
Playlist information extraction and management
"""
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import timedelta
import json
import subprocess
from pathlib import Path
from ..ui.theme import Theme
from ..ui.components import Progress, Status

@dataclass
class VideoInfo:
    """Video information container"""
    id: str
    title: str
    url: str
    duration: int
    index: Optional[int] = None
    status: str = 'pending'
    error: Optional[str] = None

class Playlist:
    """
    Playlist management with enhanced metadata
    """
    def __init__(self, url: str, theme: Theme):
        self.url = url
        self.theme = theme
        self.status = Status(theme)
        self.progress = Progress(theme)
        self.videos: List[VideoInfo] = []
        self.metadata: Dict = {}
        self._loaded = False
    
    def fetch_info(self) -> bool:
        """
        Extract comprehensive playlist information
        """
        try:
            cmd = [
                'yt-dlp',
                '--flat-playlist',
                '--dump-json',
                self.url
            ]
            
            # Show loading message
            print(self.status.info("Fetching playlist information..."))
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Parse video data
            videos = []
            total_duration = 0
            
            for line in result.stdout.strip().split('\n'):
                if line:
                    data = json.loads(line)
                    video = VideoInfo(
                        id=data['id'],
                        title=data.get('title', 'Unknown'),
                        url=f"https://www.youtube.com/watch?v={data['id']}",
                        duration=data.get('duration', 0)
                    )
                    videos.append(video)
                    total_duration += video.duration
            
            # Extract playlist metadata
            self.metadata = {
                'title': self._extract_playlist_title(),
                'video_count': len(videos),
                'total_duration': str(timedelta(seconds=total_duration)),
                'creator': self._extract_playlist_creator()
            }
            
            # Number the videos
            for i, video in enumerate(videos, 1):
                video.index = i
            
            self.videos = videos
            self._loaded = True
            
            print(self.status.success(
                f"Found {len(videos)} videos "
                f"(Total duration: {self.metadata['total_duration']})"
            ))
            return True
            
        except subprocess.CalledProcessError as e:
            print(self.status.error(
                "Failed to fetch playlist info",
                f"Error: {e.stderr}"
            ))
            return False
        except json.JSONDecodeError as e:
            print(self.status.error(
                "Failed to parse playlist data",
                f"Error: {str(e)}"
            ))
            return False
    
    def select_range(self, start: int, end: int) -> List[VideoInfo]:
        """Filter videos by range"""
        if not self._loaded:
            if not self.fetch_info():
                return []
        
        start = max(1, start)
        end = min(len(self.videos), end)
        
        selected = self.videos[start-1:end]
        print(self.status.info(
            f"Selected videos {start} to {end} ({len(selected)} videos)"
        ))
        return selected
    
    def get_failed(self) -> List[VideoInfo]:
        """Return list of failed downloads"""
        return [v for v in self.videos if v.status == 'failed']
    
    def get_successful(self) -> List[VideoInfo]:
        """Return list of successful downloads"""
        return [v for v in self.videos if v.status == 'completed']
    
    def get_pending(self) -> List[VideoInfo]:
        """Return list of pending downloads"""
        return [v for v in self.videos if v.status == 'pending']
    
    def display_info(self) -> None:
        """Display formatted playlist information"""
        if not self._loaded:
            if not self.fetch_info():
                return
        
        # Create info panel
        info = [
            ("Title", self.metadata['title']),
            ("Videos", str(self.metadata['video_count'])),
            ("Duration", self.metadata['total_duration']),
            ("Creator", self.metadata['creator'])
        ]
        
        print("\nPlaylist Information")
        print("─" * 60)
        for key, value in info:
            print(f"  {self.theme.apply_color(key + ':', 'muted')} {value}")
        print()
    
    def list_videos(self) -> None:
        """Display formatted video list"""
        if not self._loaded:
            if not self.fetch_info():
                return
        
        print("\nVideos in Playlist")
        print("─" * 60)
        
        for video in self.videos:
            duration = timedelta(seconds=video.duration)
            title_color = 'error' if video.status == 'failed' else 'text'
            
            print(f"{self.theme.apply_color(f'[{video.index:02d}]', 'muted')} "
                  f"{self.theme.apply_color(video.title, title_color)}")
            print(f"     Duration: {duration} | URL: {video.url}")
            
            if video.error:
                print(f"     {self.theme.apply_color('Error: ' + video.error, 'error')}")
            print()
    
    def _extract_playlist_title(self) -> str:
        """Extract playlist title using yt-dlp"""
        try:
            cmd = ['yt-dlp', '--get-title', '--playlist-items', '0', self.url]
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.stdout.strip() or "Unknown Playlist"
        except:
            return "Unknown Playlist"
    
    def _extract_playlist_creator(self) -> str:
        """Extract playlist creator using yt-dlp"""
        try:
            cmd = ['yt-dlp', '--get-author', '--playlist-items', '0', self.url]
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.stdout.strip() or "Unknown Creator"
        except:
            return "Unknown Creator"