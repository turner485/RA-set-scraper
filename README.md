# RetroAchievements Game Collector

RetroAchievements Game Collector is a Windows desktop application that automates searching, downloading, and organizing the most recent retail game ROMs for a wide range of classic gaming consoles. It uses the RetroAchievements API to fetch the latest achievement set claims and retrieves matching ROMs from trusted sources like Myrient and Archive.org.

![screen1](https://github.com/user-attachments/assets/885e6bf8-e9c5-4eef-bd1d-1b39597be690)

---

## Features

- **Automated Game Collection:** Fetches the most recent games with new achievement sets from RetroAchievements and downloads their ROMs.
- **Multi-Console Support:** Supports Nintendo, PlayStation, Sega, Atari, NEC, SNK, and Arcade systems.
- **ROM Search Tab:** Search, filter, and download ROMs by console and name using regex or keywords.
- **Organized Downloads:** ROMs are saved in a structured directory by console.
- **Progress Tracking:** Real-time progress bars and status updates for downloads and searches.
- **User-Friendly GUI:** Modern, tabbed interface built with PyQt5.
- **Settings Management:** Easily configure your RetroAchievements API key and download directory.
- **Standalone Executable:** Distributed as a single `.exe` file—no Python installation required.
> **Note:** This application is distributed as a standalone `.exe` file. You do **not** need to install Python or any dependencies.

## How It Works (Technical Overview)

#### Configuration
- Loads user settings (API key, download path) from a `.env` file or the Settings tab.
- Uses `config.py` for configuration management.

#### Fetching Recent Games
- Uses `api_client.py` to call the RetroAchievements API and retrieve the most recent achievement set claims.

#### Game Processing
- Filters games by user-selected consoles.
- Cleans and normalizes game titles for accurate Game searching (`utils/text_utils.py`).

#### Game Source Lookup
- Maps each console to one or more Game source URLs (`core/rom_sources.py`).
- Searches for matching Game files on Myrient and Archive.org using HTML parsing.

#### Game Downloading
- Downloads Games to the specified directory, organized by console.
- Shows download progress and handles errors gracefully (`collector_worker.py`, `utils/file_utils.py`).

### Game Search Tab
- Allows manual searching and downloading of Games by console and name (`gui/rom_search/`).
- Supports regex search, source listing, and per-Game download progress.

### GUI
- Main window with tabs for recent set collection, Game search, and settings (`gui/main_window.py`).
- Styled with custom themes (`gui/styles.py`).

Search supports collection for the following consoles:

| Nintendo                | PlayStation         | Sega                | Atari           | NEC                | Misc.      |
|-------------------------|--------------------|---------------------|-----------------|--------------------------|-------------|
| Game Boy Color          | PlayStation        | Master System       | Atari 2600      | PC Engine/TurboGrafx-16  | Arcade      |
| Game Boy                | PlayStation 2      | Game Gear           | Atari 7800      | PC Engine CD/TurboGrafx-CD|             |
| Game Boy Advance        | PlayStation Portable| Genesis/Mega Drive | Atari Jaguar    | Neo Geo CD               |             |
| NES/Famicom             |                    | Sega CD             | Atari Jaguar CD | Neo Geo Pocket           |             |
| SNES/Super Famicom      |                    | 32X                 |                 |                          |             |
| Nintendo 64             |                    | Saturn              |                 |                          |             |
| GameCube                |                    | Dreamcast           |                 |                          |             |
| Nintendo DS             |                    |                     |                 |                          |             |

---

### Usage
1. Launch the application (.exe or via python main.py).
1. Enter your RetroAchievements API key and select a download directory in the Settings tab.  
>**Your API key can be found at:**
https://retroachievements.org/settings
1. Use the "Most Recent Sets" tab to fetch and download the latest games, or use the "ROM Search" tab for manual searching.
4. Monitor progress and status in the GUI.

### Running the Executable
1. When you run the .exe; you will be greeted by this window;<br><br>
![screen2](https://github.com/user-attachments/assets/13d01658-7c8f-41e6-9a4d-c5f16cb05fac)
- Here you can define the number of roms you want and set the location in which you want to store them on your local drive. 
2. You can then filter the consoles in which the games are downloaded
<br><br>
![screen3](https://github.com/user-attachments/assets/9e84ef7b-3b05-41a3-a556-54b33ef82ee8)
3. click the start collecting button to run the application;
<br><br>
![screen4](https://github.com/user-attachments/assets/64552d00-75e5-485a-b24e-bc1c65431f0f)
4. Finally sit back, relax and wait, you can see the downloading progress in terminal;
<br><br>![screen6](https://github.com/user-attachments/assets/ca7fb9f0-66bf-4be7-a0a2-1df66d885943)
- The GUI also has a settings tab, here you can set your API key (if you haven't already done so)
<br><br>
![screen5](https://github.com/user-attachments/assets/c1fe6a15-118d-4147-acf0-c990b31e1fcd)

---

### Troubleshooting
- If Windows Defender or your antivirus flags the `.exe`, this is a common false positive for new or unsigned applications.
- If you see errors about missing DLLs, ensure you extracted all files from the release zip.
- If you have issues, please open an issue on GitHub or contact the author.
---

### Sources
[https://myrient.erista.me/](https://myrient.erista.me/)  
[https://archive.org/](https://archive.org/)
---

#### Notes
pyinstaller --noconfirm --onefile --windowed --icon=./resources/icon.ico RetroAchievement-Set-Scraper

##### Version Release Notes
- 1.1.8-Beta: Added the ability to scrape games from archive.org.
