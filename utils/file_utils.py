"""
File operation utilities
"""

import os
import requests
from pathlib import Path
from typing import Tuple, Optional, Generator
from .text_utils import clean_filename


def create_console_directory(base_path: str, console: str) -> str:
    """Create console-specific directory"""
    console_dir = os.path.join(base_path, "Games", console)
    os.makedirs(console_dir, exist_ok=True)
    return console_dir


def file_exists(filepath: str) -> bool:
    """Check if file exists"""
    return os.path.exists(filepath)


def get_file_path(base_path: str, console: str, filename: str) -> str:
    """Get full file path for a ROM"""
    console_dir = create_console_directory(base_path, console)
    cleaned_filename = clean_filename(filename)
    return os.path.join(console_dir, cleaned_filename)


def download_file(url: str, filepath: str, chunk_size: int = 8192) -> Generator[Tuple[int, int], None, None]:
    """
    Download file with progress reporting
    
    Yields:
        Tuple of (downloaded_bytes, total_bytes)
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('Content-Length', 0))
        downloaded = 0
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    yield downloaded, total_size
                    
    except requests.RequestException as e:
        # Clean up partial file on error
        if os.path.exists(filepath):
            os.remove(filepath)
        raise Exception(f"Download failed: {e}")


def get_directory_size(path: str) -> int:
    """Get total size of directory in bytes"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                total_size += os.path.getsize(filepath)
            except OSError:
                pass  # Skip files that can't be accessed
    return total_size


def ensure_directory_exists(path: str) -> None:
    """Ensure directory exists, create if not"""
    Path(path).mkdir(parents=True, exist_ok=True)


def get_available_space(path: str) -> int:
    """Get available disk space in bytes"""
    try:
        statvfs = os.statvfs(path)
        return statvfs.f_frsize * statvfs.f_bavail
    except (OSError, AttributeError):
        # Fallback for Windows
        import shutil
        return shutil.disk_usage(path).free