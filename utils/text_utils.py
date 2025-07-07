"""
Text processing utilities
"""

import re
import urllib.parse


def clean_title(raw_title: str) -> str:
    """Clean ROM title for searching"""
    title = urllib.parse.unquote(raw_title)
    title = re.sub(r'\.[a-z0-9]+$', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\s+', ' ', title)
    title = re.sub(r'[-–—]\s*$', '', title).strip()
    return title


def clean_filename(filename: str) -> str:
    """Clean filename for saving"""
    filename = urllib.parse.unquote(filename)
    filename = re.sub(r'[ \-]+', '_', filename)
    return filename


def extract_arcade_name(raw_name: str) -> str:
    """Extract arcade ROM name from raw title"""
    filename = raw_name.split()[0]
    return re.sub(r'\.[a-z0-9]+$', '', filename, flags=re.IGNORECASE)


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"


def create_progress_bar(current: int, total: int, width: int = 50) -> str:
    """Create a text-based progress bar"""
    if total == 0:
        return "░" * width
    
    percent = (current / total) * 100
    filled = int(percent * width / 100)
    bar = "█" * filled + "░" * (width - filled)
    return bar


def truncate_text(text: str, max_length: int) -> str:
    """Truncate text to maximum length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."