"""
URL validation and processing utilities
"""
import re
from typing import Tuple, Optional
from dataclasses import dataclass
from urllib.parse import urlparse, parse_qs

@dataclass
class URLInfo:
    """Container for parsed URL information"""
    url: str
    type: str  # 'video' or 'playlist'
    id: str
    is_valid: bool
    error: Optional[str] = None

class URLValidator:
    """Validate and process YouTube URLs"""
    
    # URL patterns
    VIDEO_PATTERNS = [
        r'^https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+',
        r'^https?://youtu\.be/[\w-]+',
        r'^https?://(?:www\.)?youtube\.com/embed/[\w-]+',
    ]
    
    PLAYLIST_PATTERNS = [
        r'^https?://(?:www\.)?youtube\.com/playlist\?list=[\w-]+',
        r'^https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+&list=[\w-]+',
    ]
    
    @classmethod
    def validate(cls, url: str) -> URLInfo:
        """
        Validate YouTube URL and extract information
        """
        # Clean the URL
        url = url.strip()
        
        # Check if URL is empty
        if not url:
            return URLInfo(
                url='',
                type='unknown',
                id='',
                is_valid=False,
                error='URL cannot be empty'
            )
        
        # Check for valid YouTube URL format
        try:
            parsed = urlparse(url)
            if parsed.scheme not in ('http', 'https'):
                return URLInfo(
                    url=url,
                    type='unknown',
                    id='',
                    is_valid=False,
                    error='Invalid URL scheme (must be http or https)'
                )
            
            if not any(domain in parsed.netloc 
                      for domain in ['youtube.com', 'youtu.be']):
                return URLInfo(
                    url=url,
                    type='unknown',
                    id='',
                    is_valid=False,
                    error='Not a YouTube URL'
                )
        except Exception:
            return URLInfo(
                url=url,
                type='unknown',
                id='',
                is_valid=False,
                error='Invalid URL format'
            )
        
        # Check for playlist
        for pattern in cls.PLAYLIST_PATTERNS:
            if re.match(pattern, url):
                playlist_id = cls._extract_playlist_id(url)
                if playlist_id:
                    return URLInfo(
                        url=url,
                        type='playlist',
                        id=playlist_id,
                        is_valid=True
                    )
                return URLInfo(
                    url=url,
                    type='playlist',
                    id='',
                    is_valid=False,
                    error='Could not extract playlist ID'
                )
        
        # Check for video
        for pattern in cls.VIDEO_PATTERNS:
            if re.match(pattern, url):
                video_id = cls._extract_video_id(url)
                if video_id:
                    return URLInfo(
                        url=url,
                        type='video',
                        id=video_id,
                        is_valid=True
                    )
                return URLInfo(
                    url=url,
                    type='video',
                    id='',
                    is_valid=False,
                    error='Could not extract video ID'
                )
        
        # URL doesn't match any known pattern
        return URLInfo(
            url=url,
            type='unknown',
            id='',
            is_valid=False,
            error='URL does not match any known YouTube URL pattern'
        )
    
    @staticmethod
    def _extract_video_id(url: str) -> Optional[str]:
        """Extract video ID from URL"""
        try:
            # Handle youtu.be URLs
            if 'youtu.be' in url:
                return url.split('/')[-1].split('?')[0]
            
            # Handle youtube.com URLs
            parsed = urlparse(url)
            if 'youtube.com' in parsed.netloc:
                if '/embed/' in url:
                    return url.split('/embed/')[-1].split('?')[0]
                return parse_qs(parsed.query)['v'][0]
        except:
            pass
        return None
    
    @staticmethod
    def _extract_playlist_id(url: str) -> Optional[str]:
        """Extract playlist ID from URL"""
        try:
            parsed = urlparse(url)
            return parse_qs(parsed.query)['list'][0]
        except:
            pass
        return None
    
    @staticmethod
    def normalize_url(url: str) -> str:
        """
        Normalize YouTube URL to standard format
        """
        # Convert short URLs to full format
        if 'youtu.be' in url:
            video_id = url.split('/')[-1].split('?')[0]
            return f'https://www.youtube.com/watch?v={video_id}'
        
        # Handle embed URLs
        if '/embed/' in url:
            video_id = url.split('/embed/')[-1].split('?')[0]
            return f'https://www.youtube.com/watch?v={video_id}'
        
        # Add www if missing
        if 'youtube.com' in url and not url.startswith('https://www.'):
            url = url.replace('https://', 'https://www.')
            url = url.replace('http://', 'https://www.')
        
        return url