import re

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
}

def clean_title(raw_title: str) -> str:
    # Check if angle brackets exist and extract their content
    angle_bracket_match = re.search(r'<([^>]*)>', raw_title)
    if angle_bracket_match:
        # Use content inside angle brackets as base title
        title = angle_bracket_match.group(1)
    else:
        title = raw_title

    # Remove file extension at the end of the title
    title = re.sub(r'\.[a-z0-9]+$', '', title, flags=re.IGNORECASE)

    # Remove parentheses and contents inside them
    title = re.sub(r'\([^)]*\)', '', title)

    # Remove any extra spaces
    title = title.strip()

    # Optional: Remove trailing hyphens and spaces
    title = re.sub(r'[-–—]\s*$', '', title).strip()

    return title
