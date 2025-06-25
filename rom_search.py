import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from helpers import rom_sources
import os

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
                response = requests.get(url)
                response.raise_for_status()  # Raise an error if bad response

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

                            print(f"✅ Match found: {filename}")
                            download_rom(full_url, filename)
                            found = True
                            break

                if found:
                    break  # Exit loop if we found the ROM

            except Exception as e:
                print(f"❌ Error accessing or parsing {url}: {e}")

        if not found:
            print("❌ No match found in any source.")

def download_rom(full_url, filename):
    print(f"⬇️ Downloading from {full_url} ...")
    try:
        response = requests.get(full_url)
        response.raise_for_status()

        os.makedirs("roms", exist_ok=True)
        filepath = os.path.join("roms", filename)

        with open(filepath, 'wb') as f:
            f.write(response.content)

        print(f"📥 Downloaded: {filename}")

    except Exception as e:
        print(f"❌ Failed to download {filename}: {e}")

# Load games from JSON
with open('rom_data.json') as json_file:
    games = json.load(json_file)

find_rom_url(games)
