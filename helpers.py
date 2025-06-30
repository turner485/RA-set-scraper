import re
import urllib.parse

rom_sources = {
    "PlayStation 2": [
        "https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation%202/"
    ],
    "Game Boy Advance": [
        "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Game%20Boy%20Advance/",
        "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Game%20Boy%20Advance%20(Multiboot)/",
        "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Game%20Boy%20Advance%20(Video)/",
        "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Game%20Boy%20Advance%20(e-Reader)/"
    ],
    "Nintendo 64": [
        "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Nintendo%2064%20(BigEndian)/",
        "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Nintendo%2064%20(ByteSwapped)/",
        "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Nintendo%2064DD/"
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
    "Sega CD": [
        "https://myrient.erista.me/files/Redump/Sega%20-%20Mega%20CD%20&%20Sega%20CD/"
    ],
    "Sega 32X": [
        "https://myrient.erista.me/files/No-Intro/Sega%20-%2032X/"
    ],
    "Sega Game Gear": [
        "https://myrient.erista.me/files/No-Intro/Sega%20-%20Game%20Gear/"
    ],
    "Sega Master System": [
        "https://myrient.erista.me/files/No-Intro/Sega%20-%20Master%20System%20-%20Mark%20III/"
    ],
    "Atari - 2600": [
        "https://myrient.erista.me/files/No-Intro/Sega%20-%20Saturn/"
    ],
    "Atari - 5200": [
        "https://myrient.erista.me/files/No-Intro/Atari%20-%205200/"
    ],
    "Atari - 7800": [
        "https://myrient.erista.me/files/No-Intro/Atari%20-%207800/"
    ],
    "NEC - PC Engine - TurboGrafx 16": [
        "https://myrient.erista.me/files/No-Intro/NEC%20-%20PC%20Engine%20-%20TurboGrafx-16/"
    ],
    "SNK NEO GEO CD": [
        "https://myrient.erista.me/files/Redump/SNK%20-%20Neo%20Geo%20CD/"
    ],
    "PC Engine CD/TurboGrafx-CD": [
        "https://myrient.erista.me/files/Redump/NEC%20-%20PC%20Engine%20CD%20&%20TurboGrafx%20CD/"
    ],
}

def clean_title(raw_title: str) -> str:
    # Decode URL-encoded characters (e.g., %20 → space, %28 → (, etc.)
    title = urllib.parse.unquote(raw_title)

    # Remove file extension
    title = re.sub(r'\.[a-z0-9]+$', '', title, flags=re.IGNORECASE)

    # Collapse multiple spaces into one
    title = re.sub(r'\s+', ' ', title)

    # Remove trailing dashes and spaces
    title = re.sub(r'[-–—]\s*$', '', title).strip()

    return title

def clean_filename(filename: str) -> str:
    # Decode URL-encoded characters
    filename = urllib.parse.unquote(filename)

    # Replace spaces and dashes with underscores
    filename = re.sub(r'[ \-]+', '_', filename)

    return filename
