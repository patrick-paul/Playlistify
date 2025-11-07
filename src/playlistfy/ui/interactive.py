"""
Interactive prompts and user input handling
"""
from typing import List, Optional, Any, Callable
from .theme import Theme

class Prompt:
    """User input prompts with validation and formatting"""
    
    def __init__(self, theme: Theme):
        self.theme = theme

    def input(self, question: str, default: Optional[str] = None, 
             validator: Optional[Callable[[str], bool]] = None) -> str:
        """
        Get user input with validation
        """
        arrow = self.theme.apply_color(self.theme.get_icon('arrow'), 'primary')
        
        while True:
            # Show question with default if provided
            if default:
                prompt = f"{question} (default: {default})\n{arrow} "
            else:
                prompt = f"{question}\n{arrow} "
            
            # Get input
            value = input(prompt).strip()
            
            # Handle default
            if not value and default:
                return default
            
            # Validate if validator provided
            if validator:
                try:
                    if validator(value):
                        return value
                    print(self.theme.apply_color("Invalid input. Please try again.", 'error'))
                except Exception as e:
                    print(self.theme.apply_color(f"Error: {str(e)}", 'error'))
            else:
                return value

    def select(self, question: str, options: List[str], default: int = 0) -> int:
        """
        Present a selection menu
        """
        print(f"\n{question}")
        
        # Show options
        for i, option in enumerate(options, 1):
            bullet = self.theme.get_icon('bullet')
            if i - 1 == default:
                bullet = self.theme.get_icon('check')
            print(f"{self.theme.apply_color(bullet, 'primary')} {i}. {option}")
        
        # Get selection
        while True:
            try:
                choice = self.input("\nEnter choice", str(default + 1))
                choice = int(choice)
                if 1 <= choice <= len(options):
                    return choice - 1
                print(self.theme.apply_color("Invalid choice. Please try again.", 'error'))
            except ValueError:
                print(self.theme.apply_color("Please enter a number.", 'error'))

    def confirm(self, question: str, default: bool = True) -> bool:
        """
        Yes/no confirmation
        """
        suffix = " (Y/n)" if default else " (y/N)"
        while True:
            answer = self.input(question + suffix, "y" if default else "n").lower()
            if answer in ("y", "yes"):
                return True
            if answer in ("n", "no"):
                return False
            if not answer:
                return default
            print(self.theme.apply_color("Please answer yes or no.", 'error'))

    def multi_select(self, question: str, options: List[str]) -> List[int]:
        """
        Multi-selection menu (simplified version - select by comma-separated numbers)
        Returns list of selected indices (0-based)
        """
        print(f"\n{question}")
        print(self.theme.apply_color("(Enter numbers separated by commas, e.g., 1,3,5-7)", 'muted'))

        # Show options
        for i, option in enumerate(options, 1):
            bullet = self.theme.get_icon('bullet')
            print(f"{self.theme.apply_color(bullet, 'primary')} {i}. {option}")

        # Get selections
        while True:
            try:
                choice_str = self.input("\nEnter selections")

                # Parse input (supports ranges like "1-3" and individual numbers like "1,5,7")
                selected_indices = set()
                parts = choice_str.split(',')

                for part in parts:
                    part = part.strip()
                    if '-' in part:
                        # Handle range (e.g., "1-3")
                        start, end = map(int, part.split('-'))
                        for i in range(start, end + 1):
                            if 1 <= i <= len(options):
                                selected_indices.add(i - 1)
                    else:
                        # Handle single number
                        num = int(part)
                        if 1 <= num <= len(options):
                            selected_indices.add(num - 1)

                if selected_indices:
                    return sorted(list(selected_indices))
                print(self.theme.apply_color("Please select at least one option.", 'error'))
            except ValueError:
                print(self.theme.apply_color("Invalid format. Use numbers separated by commas.", 'error'))