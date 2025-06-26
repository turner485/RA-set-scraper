import requests
import json
import os
from dotenv import load_dotenv 

load_dotenv()

api_key = os.environ.get('API_KEY')

API_URL = f"https://retroachievements.org/API/API_GetClaims.php?k=1&y={api_key}"

# Function to make a request to the API and return the JSON response
def make_request():
    r = requests.get(API_URL)
    r.raise_for_status()
    return r.json()

# retrieve the n value from the target data and add return it to a list.
def retrieve_data(data, n=10):
    return [data.pop(0) for _ in range(min(n, len(data)))]

# write the data to a file in json format
def write_to_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Wrote {len(data)} records to {filename}")

# Main function to orchestrate the request, data retrieval, and file writing
def main():
    game_data = make_request()
    first_ten = retrieve_data(game_data)
    write_to_file(first_ten, 'test.json')
    print('Written to test.json')

if __name__ == '__main__':
    main()

