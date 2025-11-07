"""
Unified dependency checking and installation
Based on playlist_downloader.py v1 implementation
"""
import sys
import subprocess
import platform
import shutil
import zipfile
import os
import time
from pathlib import Path
from typing import Optional, List, Dict, Tuple
from urllib.request import urlretrieve

from ..ui.theme import Theme
from ..ui.components import Status, Progress
from ..ui.progress import EnhancedProgress


class DependencyManager:
    """
    Manages all application dependencies (yt-dlp, ffmpeg, colorama, tqdm)
    """

    def __init__(self, theme: Theme):
        self.theme = theme
        self.status = Status(theme)
        self.progress = EnhancedProgress(theme)
        self.os_type = self._detect_os()

    def _detect_os(self) -> str:
        """Detect operating system"""
        system = platform.system().lower()
        if system == 'windows':
            return 'windows'
        elif system == 'darwin':
            return 'mac'
        elif system == 'linux':
            return 'linux'
        return 'unknown'

    def check_all(self) -> bool:
        """Check all dependencies and install if missing"""
        print("\n" + "=" * 60)
        print(self.theme.apply_color("Checking Dependencies", 'text'))
        print("=" * 60)
        print(f"\n{self.status.info(f'Detected OS: {self.os_type.upper()}')}")

        # Setup stages for progress display
        stages = [
            {'status': 'in_progress', 'message': 'Checking Python packages...'},
            {'status': 'waiting', 'message': 'Checking yt-dlp...'},
            {'status': 'waiting', 'message': 'Checking ffmpeg...'},
            {'status': 'waiting', 'message': 'Verifying installation...'}
        ]

        # Check Python packages (colorama, tqdm)
        print(f"\n[1/3] {self.status.info('Checking Python packages...')}")
        if not self._check_python_packages():
            stages[0]['status'] = 'error'
            return False
        stages[0]['status'] = 'completed'
        print(self.status.success("Python packages OK"))

        # Check yt-dlp
        print(f"\n[2/3] {self.status.info('Checking yt-dlp...')}")
        stages[1]['status'] = 'in_progress'
        if not self._check_ytdlp():
            stages[1]['status'] = 'error'
            return False
        stages[1]['status'] = 'completed'
        print(self.status.success("yt-dlp OK"))

        # Check ffmpeg
        print(f"\n[3/3] {self.status.info('Checking ffmpeg...')}")
        stages[2]['status'] = 'in_progress'
        if not self._check_ffmpeg():
            stages[2]['status'] = 'error'
            print(self.status.warning("ffmpeg not found or not accessible"))

            # Offer to install
            response = input(f"\n{self.theme.apply_color('Install ffmpeg now? (y/n): ', 'primary')}").strip().lower()
            if response == 'y':
                if self._install_ffmpeg():
                    stages[2]['status'] = 'completed'
                    print(self.status.success("ffmpeg installed successfully"))
                else:
                    stages[2]['status'] = 'error'
                    print(self.status.warning("ffmpeg installation failed - videos may download as separate files"))
            else:
                print(self.status.info("Skipping ffmpeg installation"))
                print(self.status.warning("Videos will download as separate audio/video files"))
        else:
            stages[2]['status'] = 'completed'
            print(self.status.success("ffmpeg OK"))

        # Final verification
        stages[3]['status'] = 'completed'

        print("\n" + "=" * 60)
        print(self.status.success("Dependency check complete!"))
        print("=" * 60)
        return True

    def _check_python_packages(self) -> bool:
        """Check and install required Python packages"""
        packages = ['colorama', 'tqdm', 'rich']

        for package in packages:
            try:
                __import__(package)
                print(f"  {self.status.success(f'{package} installed')}")
            except ImportError:
                print(f"  {self.status.info(f'Installing {package}...')}")
                try:
                    subprocess.check_call(
                        [sys.executable, '-m', 'pip', 'install', package],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                    print(f"  {self.status.success(f'{package} installed')}")
                except subprocess.CalledProcessError:
                    print(f"  {self.status.error(f'Failed to install {package}')}")
                    return False
        return True

    def _check_ytdlp(self) -> bool:
        """Check yt-dlp and install/update if needed"""
        if self._command_exists('yt-dlp'):
            print(f"  {self.status.success('yt-dlp found')}")
            # Try to update
            try:
                print(f"  {self.status.info('Updating to latest version...')}")
                subprocess.run(
                    [sys.executable, '-m', 'pip', 'install', '--upgrade', 'yt-dlp'],
                    capture_output=True,
                    timeout=30
                )
                print(f"  {self.status.success('Updated to latest version')}")
            except:
                pass
            return True
        else:
            print(f"  {self.status.info('yt-dlp not found - installing...')}")
            try:
                subprocess.check_call(
                    [sys.executable, '-m', 'pip', 'install', 'yt-dlp'],
                    stdout=subprocess.DEVNULL
                )
                print(f"  {self.status.success('yt-dlp installed')}")
                return True
            except subprocess.CalledProcessError:
                print(f"  {self.status.error('Failed to install yt-dlp')}")
                return False

    def _check_ffmpeg(self) -> bool:
        """Check if ffmpeg is available"""
        return self._command_exists('ffmpeg')

    def _command_exists(self, command: str) -> bool:
        """Check if a command exists in PATH"""
        # Method 1: Try shutil.which
        if shutil.which(command):
            return True

        # Method 2: Try direct execution
        try:
            result = subprocess.run(
                [command, '--version'],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            pass

        # Method 3: Check common install locations
        if self.os_type == 'windows':
            common_paths = [
                r'C:\ffmpeg\ffmpeg.exe',
                r'C:\Program Files\ffmpeg\bin\ffmpeg.exe',
                str(Path.home() / 'ffmpeg' / 'ffmpeg.exe'),
            ]
            for path in common_paths:
                if Path(path).exists():
                    return True

        return False

    def _install_ffmpeg(self) -> bool:
        """Install ffmpeg based on OS"""
        if self.os_type == 'windows':
            return self._install_ffmpeg_windows()
        elif self.os_type == 'mac':
            return self._install_ffmpeg_mac()
        elif self.os_type == 'linux':
            return self._install_ffmpeg_linux()
        return False

    def _install_ffmpeg_windows(self) -> bool:
        """Install ffmpeg on Windows"""
        print(f"\n{self.status.info('Installing ffmpeg for Windows...')}")

        # Try winget first
        if shutil.which('winget'):
            print(f"  {self.status.info('Trying winget...')}")
            try:
                subprocess.run(
                    ['winget', 'install', 'Gyan.FFmpeg', '--silent'],
                    check=True,
                    capture_output=True,
                    timeout=300
                )
                print(f"  {self.status.success('Installed via winget')}")
                return True
            except:
                print(f"  {self.status.warning('winget installation failed')}")

        # Try chocolatey
        if shutil.which('choco'):
            print(f"  {self.status.info('Trying chocolatey...')}")
            try:
                subprocess.run(
                    ['choco', 'install', 'ffmpeg', '-y'],
                    check=True,
                    capture_output=True,
                    timeout=300
                )
                print(f"  {self.status.success('Installed via chocolatey')}")
                return True
            except:
                print(f"  {self.status.warning('chocolatey installation failed')}")

        # Manual download
        print(f"  {self.status.info('Downloading manually...')}")
        try:
            ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
            install_dir = Path.home() / "ffmpeg"
            zip_path = install_dir / "ffmpeg.zip"

            install_dir.mkdir(parents=True, exist_ok=True)

            print(f"  {self.status.info('Downloading from gyan.dev...')}")
            urlretrieve(ffmpeg_url, zip_path)

            print(f"  {self.status.info('Extracting...')}")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(install_dir)

            # Find bin directory and copy executables
            bin_dirs = list(install_dir.glob("*/bin"))
            if bin_dirs:
                for exe in bin_dirs[0].glob("*.exe"):
                    shutil.copy2(exe, install_dir)

                # Try to add to PATH
                self._add_to_windows_path(str(install_dir))

                # Cleanup
                zip_path.unlink()
                for item in install_dir.iterdir():
                    if item.is_dir() and item.name.startswith('ffmpeg-'):
                        shutil.rmtree(item)

                print(f"  {self.status.success(f'Installed to {install_dir}')}")
                print(f"  {self.status.info('You may need to restart your terminal')}")
                return True
        except Exception as e:
            print(f"  {self.status.error(f'Manual installation failed: {e}')}")

        return False

    def _install_ffmpeg_mac(self) -> bool:
        """Install ffmpeg on macOS"""
        print(f"\n{self.status.info('Installing ffmpeg for macOS...')}")

        if not shutil.which('brew'):
            print(f"  {self.status.error('Homebrew not found')}")
            print("  Please install Homebrew first:")
            print('  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"')
            return False

        try:
            print(f"  {self.status.info('Installing via Homebrew...')}")
            subprocess.run(['brew', 'install', 'ffmpeg'], check=True)
            print(f"  {self.status.success('ffmpeg installed')}")
            return True
        except subprocess.CalledProcessError:
            print(f"  {self.status.error('Installation failed')}")
            return False

    def _install_ffmpeg_linux(self) -> bool:
        """Install ffmpeg on Linux"""
        print(f"\n{self.status.info('Installing ffmpeg for Linux...')}")

        # Try different package managers
        package_managers = [
            (['sudo', 'apt', 'update'], ['sudo', 'apt', 'install', '-y', 'ffmpeg']),
            (None, ['sudo', 'dnf', 'install', '-y', 'ffmpeg']),
            (None, ['sudo', 'yum', 'install', '-y', 'ffmpeg']),
            (None, ['sudo', 'pacman', '-S', '--noconfirm', 'ffmpeg']),
        ]

        for update_cmd, install_cmd in package_managers:
            try:
                if update_cmd:
                    subprocess.run(update_cmd, check=True, capture_output=True)
                subprocess.run(install_cmd, check=True)
                print(f"  {self.status.success('ffmpeg installed')}")
                return True
            except:
                continue

        print(f"  {self.status.error('Could not install automatically')}")
        print("  Please install manually:")
        print("    Ubuntu/Debian: sudo apt install ffmpeg")
        print("    Fedora: sudo dnf install ffmpeg")
        print("    Arch: sudo pacman -S ffmpeg")
        return False

    def _add_to_windows_path(self, directory: str) -> bool:
        """Add directory to Windows PATH"""
        try:
            import winreg

            # Try user PATH (doesn't require admin)
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                'Environment',
                0,
                winreg.KEY_ALL_ACCESS
            )

            current_path, _ = winreg.QueryValueEx(key, 'PATH')

            # Check if already in PATH
            path_dirs = current_path.split(';')
            if any(directory.lower() == p.lower() for p in path_dirs if p):
                winreg.CloseKey(key)
                return True

            # Add to PATH
            new_path = f"{current_path};{directory}" if current_path else directory
            winreg.SetValueEx(key, 'PATH', 0, winreg.REG_EXPAND_SZ, new_path)
            winreg.CloseKey(key)

            # Update current process
            os.environ['PATH'] = f"{os.environ['PATH']};{directory}"

            # Broadcast change
            try:
                import ctypes
                HWND_BROADCAST = 0xFFFF
                WM_SETTINGCHANGE = 0x1A
                SendMessageTimeoutW = ctypes.windll.user32.SendMessageTimeoutW
                SendMessageTimeoutW(HWND_BROADCAST, WM_SETTINGCHANGE, 0, 'Environment', 0x0002, 5000, ctypes.c_long())
            except:
                pass

            print(f"  {self.status.success(f'Added {directory} to PATH')}")
            return True
        except Exception as e:
            print(f"  {self.status.warning(f'Could not add to PATH: {e}')}")
            print(f"\n  Please add manually: {directory}")
            return False
