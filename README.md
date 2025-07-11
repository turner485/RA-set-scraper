# RetroAchievements most recent set game collector 1.1.9-Beta
This RetroAchievement new set game collector will search & download new games and organise them by console, due to the complexity and sheer amount of "faff" 😆 this application will only download RETAIL games, all hacks, unlicensed & homebrews will not be downloaded.<br/><br/>
![screen1](https://github.com/user-attachments/assets/885e6bf8-e9c5-4eef-bd1d-1b39597be690)

> **Note:** This application is distributed as a standalone `.exe` file. You do **not** need to install Python or any dependencies.

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

### Requirements

- Windows 10 or later
- Internet connection

### Setup :gear:
1. Run RetroAchievement-Set-Scraper.exe
2. Navigate to settings tab
3. Add your RetroAchievements API key
**Your API key can be found at:**
https://retroachievements.org/settings
4. Browse for your destination directory
5. Done!!!
---


### Running the Executable 🏃
1. When you run the .exe; you will be greeted by this window;<br><br>
![screen2](https://github.com/user-attachments/assets/13d01658-7c8f-41e6-9a4d-c5f16cb05fac)
- Here you can define the number of roms you want and set the location in which you want to store them on your local drive. 📁📁📁
2. You can then filter the consoles in which the games are downloaded 🎮🎮
<br><br>
![screen3](https://github.com/user-attachments/assets/9e84ef7b-3b05-41a3-a556-54b33ef82ee8)
3. click the start collecting button to run the application 🚀🚀🚀;
<br><br>
![screen4](https://github.com/user-attachments/assets/64552d00-75e5-485a-b24e-bc1c65431f0f)
4. Finally sit back, relax and wait, you can see the downloading progress in terminal ☕☕☕;
<br><br>![screen6](https://github.com/user-attachments/assets/ca7fb9f0-66bf-4be7-a0a2-1df66d885943)
- The GUI also has a settings tab, here you can set your API key (if you haven't already done so) ⚙️⚙️
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
pyinstaller --onefile --windowed --icon=resources/ra-logo.ico --add-data "resources;resources" main.py
##### Version Release Notes
- 1.1.8-Beta: Added the ability to scrape games from archive.org.
- 1.1.9-Beta: Add ico file