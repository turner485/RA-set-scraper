from make_request import write_to_file
from helpers import *
import json
import requests
import os
from dotenv import load_dotenv  
load_dotenv()
import time

api_key = os.environ.get('API_KEY')

# Initialize the game dictionary to store games, consoles, and their hashes
game_dict = {
    'games': [],
    'consoles': [],
    'gameHashes': []
}

# Initialize lists to store URLs, hashes, and titles
game_urls = []
game_hash_list = []
game_title_list = []

# Creates a list of game hashes and urls to be used later, using data from a JSON file.x
def read_from_json(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
        for game in data:
            time.sleep(1)
            game_id = game['GameID']
            console_name = game['ConsoleName']
            game_hash_url = f"https://retroachievements.org/API/API_GetGameHashes.php?i={game_id}&y={api_key}"
            game_dict['games'].append(game_id)
            game_dict['consoles'].append(console_name)
            game_dict['gameHashes'].append(game_hash_url)
            game_urls.append(game_hash_url)
    return game_urls

def read_from_url(single_game_urls):
    for url, console in zip(single_game_urls, game_dict['consoles']):
        try:
            r = requests.get(url)
            r.raise_for_status()
            data = r.json()
            game_hash_list.append(data)

            results = data.get('Results', [])
            if not results:
                game_title_list.append('Unknown')
                continue

            # Filter out patched ROMs (PatchUrl is not None)
            clean_results = [res for res in results if not res.get('PatchUrl')]

            if len(clean_results) == 0:
                # No clean ROMs, fallback to all results
                selected_result = results[0]
            elif len(clean_results) == 1:
                selected_result = clean_results[0]
            else:
                # Multiple clean results, pick the first (or apply further logic if needed)
                selected_result = clean_results[0]

            raw_name = selected_result.get('Name', 'Unknown Title')

            if console == "Arcade":
                filename = raw_name.split()[0]
                rom_base_name = re.sub(r'\.[a-z0-9]+$', '', filename, flags=re.IGNORECASE)
            else:
                rom_base_name = clean_title(raw_name)
                print(f"Retrieving ROM Base Name: {rom_base_name} for {console}")

            game_title_list.append(rom_base_name.strip())

            time.sleep(0.5)

        except Exception as e:
            print(f"Failed to fetch or parse: {url}\nError: {e}")
            game_title_list.append('Error')

    return game_title_list


def search_for_rom(game_titles, consoles):
    rom_data = []
    for title, console in zip(game_titles, consoles):
        rom_data.append({"title": title, "console": console})
    return rom_data

# Call sequence
read_from_json("./data/most_recent_claim.json")
read_from_url(game_urls)
search_for_rom(game_title_list, game_dict['consoles'])
roms_data = search_for_rom(game_title_list, game_dict['consoles'])
write_to_file(roms_data, './data/rom_data.json')
