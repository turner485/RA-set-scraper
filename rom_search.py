
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

rom_sources = {
    "Game Boy Advance": "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Game%20Boy%20Advance/",
    "Game Boy Color": "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Game%20Boy%20Color/",
    "Nintendo - Game Boy": "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Game%20Boy/",
    "Nintendo - Super Nintendo Entertainment System": "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Super%20Nintendo%20Entertainment%20System/",
    "NES/Famicom": "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Nintendo%20Entertainment%20System%20(Headered)/",
    "Arcade": "https://myrient.erista.me/files/Internet%20Archive/chadmaster/fbnarcade-fullnonmerged/arcade/"
}

def find_rom_url(games):
    for game in games:
        console = game['console']
        title = game['title']

        source_url = rom_sources.get(console)
        if not source_url:
            print(f"⚠️ No ROM source for console: {console}")
            continue

        print(f"\n🔍 Searching for: {title}")
        try:
            response = requests.get(source_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            td_tags = soup.find_all('td', class_='link')

            found = False
            for td in td_tags:
                a_tag = td.find('a')
                if a_tag:
                    link_title = a_tag.get('title') or a_tag.text  # Prefer title attribute, fallback to text
                    href = a_tag.get('href')

                    # Normalize casing for comparison
                    if title.lower() in link_title.lower():
                        full_url = urljoin(source_url, href)
                        filename = os.path.basename(href)

                        print(f"✅ Match found: {filename}")
                        download_rom(full_url, filename)
                        found = True
                        break

            if not found:
                print("❌ No match found on page.")

        except Exception as e:
            print(f"🚨 Error while processing '{title}': {e}")

def download_rom(full_url, filename):
    print(f"⬇️ Downloading from {full_url} ...")
    try:
        response = requests.get(full_url)
        response.raise_for_status()

        # Ensure the /roms directory exists
        os.makedirs("roms", exist_ok=True)

        # Write the file to the directory
        filepath = os.path.join("roms", filename)
        with open(filepath, 'wb') as f:
            f.write(response.content)

        print(f"📥 Downloaded: {filename}")

    except Exception as e:
        print(f"❌ Failed to download {filename}: {e}")

with open('rom_data.json') as json_file:
    games = json.load(json_file)

find_rom_url(games)