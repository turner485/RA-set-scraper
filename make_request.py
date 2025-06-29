import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get('API_KEY')
API_URL = f"https://retroachievements.org/API/API_GetClaims.php?k=1&y={api_key}"

def make_request():
    r = requests.get(API_URL)
    r.raise_for_status()
    return r.json()

# Find the most recent claim based on DoneTime
def get_top_n_recent_by_donetime(data, n=10):
    # Ensure DoneTime exists and sort in descending order
    sorted_data = sorted(
        data,
        key=lambda entry: entry.get("DoneTime", ""),
        reverse=True
    )
    return sorted_data[:n]

def write_to_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def main():
    game_data = make_request()
    most_recent = get_top_n_recent_by_donetime(game_data)
    write_to_file(most_recent, './data/most_recent_claim.json')
    print('Most recent claim written to most_recent_claim.json')

if __name__ == '__main__':
    main()
