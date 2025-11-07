"""
Smart retry logic with exponential backoff and error-specific handling
"""
import time
import random
from functools import wraps
from typing import Tuple, Optional, Type, Union, Callable
from .errors import DownloadError

class RetryStrategy:
    """Context-aware retry logic with smart backoff"""
    
    ERROR_STRATEGIES = {
        'bot_detection': {
            'max_attempts': 2,
            'base_delay': 60,
            'jitter': 0.2
        },
        'network_error': {
            'max_attempts': 5,
            'base_delay': 3,
            'jitter': 0.1
        },
        'merge_failed': {
            'max_attempts': 3,
            'base_delay': 5,
            'jitter': 0.1
        }
    }
    
    @classmethod
    def should_retry(cls, error: Exception, attempt: int) -> Tuple[bool, float]:
        """
        Determine whether to retry based on error type and attempt number
        Returns: (should_retry, delay_seconds)
        """
        # Handle DownloadError specifically
        if isinstance(error, DownloadError):
            error_type = cls._categorize_error(error)
            strategy = cls.ERROR_STRATEGIES.get(error_type, {
                'max_attempts': 3,
                'base_delay': 5,
                'jitter': 0.1
            })
            
            if attempt < strategy['max_attempts']:
                delay = cls._calculate_delay(
                    attempt,
                    strategy['base_delay'],
                    strategy['jitter']
                )
                return True, delay
            return False, 0
        
        # Generic error handling
        if attempt < 3:
            return True, cls._calculate_delay(attempt, 5, 0.1)
        return False, 0
    
    @staticmethod
    def _categorize_error(error: DownloadError) -> str:
        """Categorize error for retry strategy selection"""
        message = error.message.lower()
        
        if 'bot' in message or '429' in message:
            return 'bot_detection'
        elif 'network' in message or 'connection' in message:
            return 'network_error'
        elif 'merge' in message or 'ffmpeg' in message:
            return 'merge_failed'
        return 'generic'
    
    @staticmethod
    def _calculate_delay(attempt: int, base_delay: float, jitter: float) -> float:
        """Calculate delay with exponential backoff and jitter"""
        delay = base_delay * (2 ** (attempt - 1))  # Exponential backoff
        max_jitter = delay * jitter
        actual_jitter = random.uniform(0, max_jitter)
        return delay + actual_jitter

def retry(
    max_attempts: int = 3,
    exceptions: Union[Type[Exception], Tuple[Type[Exception], ...]] = Exception,
    on_retry: Optional[Callable[[Exception, int], None]] = None
) -> Callable:
    """
    Decorator for automatic retries with smart backoff
    
    Args:
        max_attempts: Maximum number of retry attempts
        exceptions: Exception types to catch
        on_retry: Callback function for retry events
    
    Example:
    @retry(max_attempts=3, exceptions=(NetworkError, TimeoutError))
    def download_video(url):
        # Implementation
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    
                    # Check if we should retry
                    should_retry, delay = RetryStrategy.should_retry(e, attempt)
                    
                    if should_retry and attempt < max_attempts:
                        # Notify callback if provided
                        if on_retry:
                            on_retry(e, attempt)
                        
                        # Wait before retry
                        time.sleep(delay)
                        continue
                    
                    # If we shouldn't retry or exceeded attempts, raise the last error
                    raise last_exception
            
            # This shouldn't be reached, but raise the last exception just in case
            if last_exception:
                raise last_exception
        
        return wrapper
    return decorator