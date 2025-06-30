import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from helpers import rom_sources, clean_filename
from rich.progress import Progress
import requests
import os
import time

def find_rom_url(games):
    for game in games:
        console = game['console']
        title = game['title']

        source_urls = rom_sources.get(console)

        if not source_urls:
            print(f"⚠️ No ROM source for console: {console}")
            continue

        # Make sure it's a list
        if isinstance(source_urls, str):
            source_urls = [source_urls]

        print(f"\n🔍 Searching for: {title}")
        found = False

        for url in source_urls:
            try:
                time.sleep(0.5)
                response = requests.get(url)
                response.raise_for_status()

                print(f"🌐 Accessing: {url}")
                soup = BeautifulSoup(response.content, 'html.parser')
                td_tags = soup.find_all('td', class_='link')

                for td in td_tags:
                    a_tag = td.find('a')
                    if a_tag:
                        link_title = a_tag.get('title') or a_tag.text
                        href = a_tag.get('href')

                        if title.lower() in link_title.lower():
                            full_url = urljoin(url, href)
                            filename = os.path.basename(href)
                            filename = clean_filename(filename)
                            print(f"✅ Match found: {filename}")
                            download_rom(full_url, filename, game)  # Pass the current game
                            found = True
                            break
                if found:
                    break  

            except Exception as e:
                print(f"❌ Error accessing or parsing {url}: {e}")

        if not found:
            print("❌ No match found in any source.")

def download_rom(full_url, filename, game):
    console = game['console']
    print(f"⬇️ Downloading from {full_url} ...")
    try:
        response = requests.get(full_url, stream=True)
        response.raise_for_status()

        # Create directory for the console
        os.makedirs(os.path.join("roms", console), exist_ok=True)

        filename = clean_filename(filename)
        filepath = os.path.join("roms", console, filename)

        # Check if file already exists
        if os.path.exists(filepath):
            print(f"⚠️ Skipped (already downloaded): {filename}")
            return

        total_size = int(response.headers.get('Content-Length', 0))

        with open(filepath, 'wb') as f, Progress() as progress:
            task = progress.add_task(f"📥 {filename}", total=total_size)

            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    progress.update(task, advance=len(chunk))

        print(f"✅ Downloaded: {filename}")

    except Exception as e:
        print(f"❌ Failed to download {filename}: {e}")

with open('./data/rom_data.json') as json_file:
    games = json.load(json_file)

find_rom_url(games)
