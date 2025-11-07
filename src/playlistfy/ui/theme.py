"""
Theme management system for Playlistfy
"""
import sys
from typing import Dict, Any
from colorama import Fore, Style, init

init(autoreset=True)

# Use safe ASCII characters on Windows to avoid encoding issues
USE_SAFE_CHARS = sys.platform == 'win32'

class Theme:
    """
    Theme system with support for multiple color schemes
    """
    # Use safe ASCII or Unicode based on platform
    if USE_SAFE_CHARS:
        BORDERS = {
            'top_left': '+', 'top_right': '+',
            'bottom_left': '+', 'bottom_right': '+',
            'horizontal': '-', 'vertical': '|',
            'divider': '-',
            'tree_stem': '|', 'tree_branch': '-',
            'tree_last': '+', 'tree_space': ' '
        }
        ICONS = {
            'success': '[OK]', 'error': '[X]', 'warning': '[!]',
            'info': '[i]', 'download': 'v', 'check': '*',
            'process': 'o', 'bullet': '*', 'arrow': '>',
            'loading': ['|', '/', '-', '\\']
        }
    else:
        BORDERS = {
            'top_left': '┌', 'top_right': '┐',
            'bottom_left': '└', 'bottom_right': '┘',
            'horizontal': '─', 'vertical': '│',
            'divider': '─',
            'tree_stem': '├', 'tree_branch': '─',
            'tree_last': '└', 'tree_space': ' '
        }
        ICONS = {
            'success': '✓', 'error': '✗', 'warning': '⚠',
            'info': 'ℹ', 'download': '↓', 'check': '◆',
            'process': '○', 'bullet': '•', 'arrow': '›',
            'loading': ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        }

    COLORS = {
        'primary': Fore.CYAN + Style.BRIGHT,
        'success': Fore.GREEN + Style.BRIGHT,
        'warning': Fore.YELLOW + Style.BRIGHT,
        'error': Fore.RED + Style.BRIGHT,
        'info': Fore.BLUE + Style.BRIGHT,
        'muted': Fore.WHITE,
        'text': Style.BRIGHT + Fore.WHITE,
        'reset': Style.RESET_ALL,
        'highlight': Fore.CYAN + Style.BRIGHT
    }

    def __init__(self, theme_name: str = 'dark'):
        """Initialize theme with given name"""
        self.theme_name = theme_name
        self.borders = self.BORDERS
        self.colors = self.COLORS
        self.icons = self.ICONS

    def apply_color(self, text: str, color: str) -> str:
        """Apply color to text"""
        return f"{self.colors.get(color, '')}{text}{self.colors['reset']}"

    def get_icon(self, name: str) -> str:
        """Get icon by name"""
        return self.icons.get(name, '')

    def style(self, text: str, style_name: str) -> str:
        """Apply style to text (alias for apply_color for compatibility)"""
        return self.apply_color(text, style_name)