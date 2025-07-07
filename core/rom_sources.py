"""
ROM source definitions and console mappings
"""

from typing import Dict, List

# ROM source URLs organized by console
ROM_SOURCES: Dict[str, List[str]] = {
    # Nintendo consoles
    "Game Boy Color": [
        "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Game%20Boy%20Color/"
    ],
    "Game Boy": [
        "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Game%20Boy/"
    ],
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
    "SNES/Super Famicom": [
        "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Super%20Nintendo%20Entertainment%20System/"
    ],
    "Nintendo 64": [
        "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Nintendo%2064%20(BigEndian)/",
        "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Nintendo%2064%20(ByteSwapped)/",
        "https://myrient.erista.me/files/Internet%20Archive/Unknown/RedumpNintendoGameCubeAmericaPart3/",
        "https://myrient.erista.me/files/Internet%20Archive/kodi_amp_spmc_canada/EuropeanGamecubeCollectionByGhostware/"
    ],
    "GameCube": [
        "https://myrient.erista.me/files/Internet%20Archive/Unknown/RedumpNintendoGameCubeAmerica/",
        "https://myrient.erista.me/files/Internet%20Archive/Unknown/RedumpNintendoGameCubeAmericaPart2/",
        "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Nintendo%20DS%20(Download%20Play)/"
    ],
    "Nintendo DS": [
        "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Nintendo%20DS%20(Decrypted)/",
        "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Nintendo%20DS%20(Encrypted)/",
        "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Nintendo%20DS%20(Download%20Play)/"
    ],
    
    # Sony consoles
    "PlayStation": [
        "https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation/"
    ],
    "PlayStation 2": [
        "https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation%202/"
    ],
    "PlayStation Portable": [
        "https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation%20Portable/"
    ],
    
    # Atari consoles
    "Atari 2600": [
        "https://myrient.erista.me/files/No-Intro/Atari%20-%202600/"
    ],
    "Atari 7800": [
        "https://myrient.erista.me/files/No-Intro/Atari%20-%207800/"
    ],
    "Atari Jaguar": [
        "https://myrient.erista.me/files/Internet%20Archive/chadmaster/jagcd-chd-zstd/jagcd-chd-zstd/"
    ],
    "Atari Jaguar CD": [
        "https://myrient.erista.me/files/Redump/Atari%20-%20Jaguar%20CD%20Interactive%20Multimedia%20System/"
    ],
    
    # Sega consoles
    "Master System": [
        "https://myrient.erista.me/files/No-Intro/Sega%20-%20Master%20System%20-%20Mark%20III/"
    ],
    "Game Gear": [
        "https://myrient.erista.me/files/No-Intro/Sega%20-%20Game%20Gear/"
    ],
    "Genesis/Mega Drive": [
        "https://myrient.erista.me/files/No-Intro/Sega%20-%20Mega%20Drive%20-%20Genesis/"
    ],
    "Sega CD": [
        "https://myrient.erista.me/files/Redump/Sega%20-%20Mega%20CD%20&%20Sega%20CD/"
    ],
    "32X": [
        "https://myrient.erista.me/files/No-Intro/Sega%20-%2032X/"
    ],
    "Saturn": [
        "https://myrient.erista.me/files/Internet%20Archive/chadmaster/chd_saturn/CHD-Saturn/USA/",
        "https://myrient.erista.me/files/Internet%20Archive/chadmaster/chd_saturn/CHD-Saturn/Japan/"
    ],
    "Dreamcast": [
        "https://myrient.erista.me/files/Internet%20Archive/chadmaster/dc-chd-zstd-redump/dc-chd-zstd/"
    ],
    
    # NEC consoles
    "PC Engine/TurboGrafx-16": [
        "https://myrient.erista.me/files/No-Intro/NEC%20-%20PC%20Engine%20-%20TurboGrafx-16/"
    ],
    "PC Engine CD/TurboGrafx-CD": [
        "https://myrient.erista.me/files/Redump/NEC%20-%20PC%20Engine%20CD%20&%20TurboGrafx%20CD/"
    ],
    
    # SNK consoles
    "Neo Geo CD": [
        "https://myrient.erista.me/files/Redump/SNK%20-%20Neo%20Geo%20CD/"
    ],
    "Neo Geo Pocket": [
        "https://myrient.erista.me/files/No-Intro/SNK%20-%20NeoGeo%20Pocket%20Color/"
    ],
    
    # Arcade
    "Arcade": [
        "https://myrient.erista.me/files/Internet%20Archive/chadmaster/fbnarcade-fullnonmerged/arcade/"
    ]
}


def get_supported_consoles() -> List[str]:
    """Get list of supported console names"""
    return list(ROM_SOURCES.keys())


def get_console_sources(console: str) -> List[str]:
    """Get ROM sources for a specific console"""
    return ROM_SOURCES.get(console, [])


def is_console_supported(console: str) -> bool:
    """Check if a console is supported"""
    return console in ROM_SOURCES