import re
import urllib.parse
rom_sources = {
    "Game Boy Advance": [
        "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Game%20Boy%20Advance/",
        "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Game%20Boy%20Advance%20(Multiboot)/",
        "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Game%20Boy%20Advance%20(Video)/",
        "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Game%20Boy%20Advance%20(e-Reader)/"
    ],
    "NES/Famicom": [
        "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Nintendo%20Entertainment%20System%20(Headered)/",
        "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Nintendo%20Entertainment%20System%20(Headerless)/"
    ],
    "Arcade": [
        "https://myrient.erista.me/files/Internet%20Archive/chadmaster/fbnarcade-fullnonmerged/arcade/"
    ],
    "Game Boy Color": [
        "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Game%20Boy%20Color/"
    ],
    "Nintendo - Game Boy": [
        "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Game%20Boy/"
    ],
    "SNES/Super Famicom": [
        "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Super%20Nintendo%20Entertainment%20System/"
    ],
    "Genesis/Mega Drive": [
        "https://myrient.erista.me/files/No-Intro/Sega%20-%20Mega%20Drive%20-%20Genesis/"
    ],
    
}

def clean_title(raw_title: str) -> str:
    # Decode URL-encoded characters (e.g., %20 → space, %28 → (, etc.)
    title = urllib.parse.unquote(raw_title)

    # Extract content inside angle brackets (if present)
    angle_bracket_match = re.search(r'<([^>]*)>', title)
    if angle_bracket_match:
        title = angle_bracket_match.group(1)

    # Remove file extension
    title = re.sub(r'\.[a-z0-9]+$', '', title, flags=re.IGNORECASE)

    # Remove contents inside parentheses or brackets
    title = re.sub(r'\([^)]*\)', '', title)  # remove (content)
    title = re.sub(r'\[[^\]]*\]', '', title)  # optionally remove [content] too

    # Collapse multiple spaces into one
    title = re.sub(r'\s+', ' ', title)

    # Remove trailing dashes and spaces
    title = re.sub(r'[-–—]\s*$', '', title).strip()

    return title

def clean_filename(filename: str) -> str:
    # Decode URL-encoded characters
    filename = urllib.parse.unquote(filename)

    # Remove contents inside parentheses or brackets
    filename = re.sub(r'\([^)]*\)', '', filename)
    filename = re.sub(r'\[[^\]]*\]', '', filename)

    # Collapse multiple spaces into one
    filename = re.sub(r'\s+', ' ', filename).strip()

    # Replace spaces and dashes with underscores
    filename = re.sub(r'[ \-]+', '_', filename)

    # Remove leading/trailing underscores
    filename = filename.strip('_')

    return filename
