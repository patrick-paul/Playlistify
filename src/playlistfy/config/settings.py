"""
Application configuration management
Hierarchical: defaults → global config → project config → env vars → CLI args
"""
import os
import json
from pathlib import Path
from typing import Any, Dict, Optional
from dataclasses import dataclass, asdict


@dataclass
class Config:
    """Application configuration with defaults"""
    output_dir: str = "downloads"
    quality: str = "best"
    parallel_workers: int = 3
    max_retries: int = 3
    theme: str = "dark"
    use_cookies: Optional[str] = None
    archive_file: str = ".playlistfy_archive"
    rate_limit: Optional[str] = None
    prefer_format: str = "mp4"
    browser_for_cookies: Optional[str] = None

    # "Don't ask again" flags
    ask_quality: bool = True
    ask_download_dir: bool = True
    ask_parallel_mode: bool = True
    ask_num_workers: bool = True

    # Default download mode
    use_parallel: bool = True

    @classmethod
    def load(cls) -> 'Config':
        """
        Load configuration from all sources in order of precedence
        """
        config = cls()  # Start with defaults

        # Load from global config file
        global_config_path = Path.home() / '.playlistfy' / 'config.json'
        if global_config_path.exists():
            config._update_from_file(global_config_path)

        # Load from project config file
        project_config_path = Path.cwd() / 'playlistfy.json'
        if project_config_path.exists():
            config._update_from_file(project_config_path)

        # Load from environment variables
        config._update_from_env()

        return config

    def _update_from_file(self, file_path: Path) -> None:
        """Update configuration from JSON file"""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                for key, value in data.items():
                    if hasattr(self, key):
                        setattr(self, key, value)
        except Exception:
            pass  # Silently ignore config file errors

    def _update_from_env(self) -> None:
        """Update configuration from environment variables"""
        env_mapping = {
            'PLAYLISTFY_OUTPUT_DIR': 'output_dir',
            'PLAYLISTFY_QUALITY': 'quality',
            'PLAYLISTFY_WORKERS': 'parallel_workers',
            'PLAYLISTFY_RETRIES': 'max_retries',
            'PLAYLISTFY_THEME': 'theme',
            'PLAYLISTFY_COOKIES': 'use_cookies',
        }

        for env_var, attr_name in env_mapping.items():
            value = os.getenv(env_var)
            if value:
                # Convert to appropriate type
                attr_type = type(getattr(self, attr_name))
                if attr_type == int:
                    try:
                        setattr(self, attr_name, int(value))
                    except ValueError:
                        pass
                else:
                    setattr(self, attr_name, value)

    def save(self, global_config: bool = True) -> None:
        """
        Save current configuration to file

        Args:
            global_config: If True, save to global config (~/.playlistfy/config.json)
                         If False, save to project config (./playlistfy.json)
        """
        if global_config:
            config_path = Path.home() / '.playlistfy' / 'config.json'
            config_path.parent.mkdir(parents=True, exist_ok=True)
        else:
            config_path = Path.cwd() / 'playlistfy.json'

        try:
            with open(config_path, 'w') as f:
                json.dump(asdict(self), f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save configuration: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return getattr(self, key, default)

    def set(self, key: str, value: Any) -> None:
        """Set configuration value"""
        if hasattr(self, key):
            setattr(self, key, value)

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return asdict(self)

    def reset_to_defaults(self) -> None:
        """Reset all settings to their default values"""
        defaults = Config()
        for key, value in asdict(defaults).items():
            setattr(self, key, value)

    def set_default(self, key: str, value: Any, dont_ask_again: bool = False) -> None:
        """
        Set a default value and optionally disable prompting for it

        Args:
            key: The setting key
            value: The value to set
            dont_ask_again: If True, disable prompting for this setting
        """
        if hasattr(self, key):
            setattr(self, key, value)

            # Update the corresponding "ask" flag if it exists
            if dont_ask_again:
                ask_key = f"ask_{key}"
                if hasattr(self, ask_key):
                    setattr(self, ask_key, False)
