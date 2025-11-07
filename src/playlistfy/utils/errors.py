"""
Enhanced error handling system
"""
import re
from typing import List, Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class DownloadError(Exception):
    """Enhanced error with context and recovery suggestions"""
    message: str
    video: Optional[Dict[str, Any]] = None
    cause: Optional[Exception] = None
    suggestions: List[str] = None

    def __post_init__(self):
        if self.suggestions is None:
            self.suggestions = []
        super().__init__(self.message)

class ErrorHandler:
    """Centralized error handling with user-friendly messages"""
    
    ERROR_PATTERNS = {
        'bot_detection': {
            'pattern': r'Sign in to confirm|bot.*detected',
            'message': 'YouTube detected automated access',
            'suggestions': [
                'Use --cookies-from-browser chrome',
                'Log into YouTube in your browser first',
                'Wait a few minutes and try again',
                'Use a VPN if you\'re rate-limited'
            ]
        },
        'video_unavailable': {
            'pattern': r'Video unavailable|Private video',
            'message': 'This video cannot be accessed',
            'suggestions': [
                'Check if the video is private or deleted',
                'Verify the URL is correct',
                'Try accessing the video in your browser first'
            ]
        },
        'network_error': {
            'pattern': r'Connection.*refused|timeout|unreachable',
            'message': 'Network connection failed',
            'suggestions': [
                'Check your internet connection',
                'Try again in a few moments',
                'Check if YouTube is accessible',
                'Disable VPN/proxy if active'
            ]
        },
        'rate_limit': {
            'pattern': r'429|Too many requests',
            'message': 'Rate limit exceeded',
            'suggestions': [
                'Wait a few minutes before trying again',
                'Reduce number of parallel downloads',
                'Try using browser cookies',
                'Use a different IP address'
            ]
        }
    }
    
    def __init__(self, theme):
        """Initialize with UI theme"""
        self.theme = theme

    def analyze_error(self, error: Exception) -> DownloadError:
        """Analyze error and return enhanced error info"""
        error_str = str(error).lower()
        
        # Check against known patterns
        for error_type, info in self.ERROR_PATTERNS.items():
            if re.search(info['pattern'], error_str, re.IGNORECASE):
                return DownloadError(
                    message=info['message'],
                    cause=error,
                    suggestions=info['suggestions']
                )
        
        # Generic error
        return DownloadError(
            message=str(error),
            cause=error,
            suggestions=['Try the operation again', 'Check the logs for more details']
        )

    def format_error(self, error: DownloadError) -> str:
        """Format error for display"""
        # Main error message
        result = [
            self.theme.apply_color(f"✗ Error: {error.message}", 'error')
        ]
        
        # Add video context if available
        if error.video:
            video_info = f"Video: {error.video.get('title', 'Unknown')}"
            if 'index' in error.video:
                video_info += f" (Video {error.video['index']})"
            result.append(self.theme.apply_color(video_info, 'muted'))
        
        # Add suggestions
        if error.suggestions:
            result.append("\nSuggestions:")
            for i, suggestion in enumerate(error.suggestions, 1):
                result.append(f"  {i}. {suggestion}")
        
        return "\n".join(result)