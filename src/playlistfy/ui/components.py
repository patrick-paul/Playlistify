"""
UI components for Playlistfy
"""
import shutil
import time
from typing import List, Dict, Any, Optional, Callable
from .theme import Theme

class Box:
    """Create bordered boxes and sections"""
    
    def __init__(self, theme: Theme):
        self.theme = theme
        self.width = shutil.get_terminal_size().columns - 4

    def header(self, title: str, subtitle: Optional[str] = None) -> str:
        """Create header box with optional subtitle"""
        width = min(self.width, 80)
        
        # Create top border
        result = [
            f"{self.theme.borders['top_left']}{self.theme.borders['horizontal'] * (width-2)}{self.theme.borders['top_right']}"
        ]
        
        # Add title
        title_line = f"{self.theme.borders['vertical']} {self.theme.apply_color(title, 'text')}"
        title_line += " " * (width - len(title) - 3)
        title_line += self.theme.borders['vertical']
        result.append(title_line)
        
        # Add subtitle if provided
        if subtitle:
            sub_line = f"{self.theme.borders['vertical']} {self.theme.apply_color(subtitle, 'muted')}"
            sub_line += " " * (width - len(subtitle) - 3)
            sub_line += self.theme.borders['vertical']
            result.append(sub_line)
        
        # Add bottom border
        result.append(
            f"{self.theme.borders['bottom_left']}{self.theme.borders['horizontal'] * (width-2)}{self.theme.borders['bottom_right']}"
        )
        
        return "\n".join(result)

    def section(self, title: str) -> str:
        """Create a section divider with title"""
        width = min(self.width, 80)
        title = f" {title} "
        padding = self.theme.borders['horizontal'] * ((width - len(title)) // 2)
        return f"\n{padding}{self.theme.apply_color(title, 'primary')}{padding}\n"

class Progress:
    """Progress indicators and spinners"""
    
    def __init__(self, theme: Theme):
        self.theme = theme
        self.spinner_index = 0
        self.last_update = time.time()

    def bar(self, current: int, total: int, prefix: str = "", width: int = 40) -> str:
        """Create progress bar"""
        percentage = current / total
        filled = int(width * percentage)
        empty = width - filled
        
        bar = "█" * filled + "░" * empty
        percent = f"{int(percentage * 100):3d}%"
        
        return (
            f"{self.theme.apply_color(prefix, 'text')} "
            f"[{self.theme.apply_color(bar, 'primary')}] "
            f"{self.theme.apply_color(percent, 'text')} "
            f"({current}/{total})"
        )

    def spinner(self, text: str) -> str:
        """Animated spinner with text"""
        now = time.time()
        if now - self.last_update > 0.1:  # Update every 100ms
            self.spinner_index = (self.spinner_index + 1) % len(self.theme.icons['loading'])
            self.last_update = now
            
        spinner = self.theme.icons['loading'][self.spinner_index]
        return f"{self.theme.apply_color(spinner, 'primary')} {text}"

class Status:
    """Status message formatting"""
    
    def __init__(self, theme: Theme):
        self.theme = theme

    def success(self, message: str) -> str:
        """Format success message"""
        return f"{self.theme.apply_color(self.theme.get_icon('success'), 'success')} {message}"

    def error(self, message: str, details: Optional[str] = None) -> str:
        """Format error message with optional details"""
        error = f"{self.theme.apply_color(self.theme.get_icon('error'), 'error')} {message}"
        if details:
            error += f"\n  {self.theme.borders['tree_last']}─ {self.theme.apply_color(details, 'muted')}"
        return error

    def info(self, message: str) -> str:
        """Format info message"""
        return f"{self.theme.apply_color(self.theme.get_icon('info'), 'info')} {message}"

    def warning(self, message: str) -> str:
        """Format warning message"""
        return f"{self.theme.apply_color(self.theme.get_icon('warning'), 'warning')} {message}"