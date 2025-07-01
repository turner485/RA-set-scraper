# RA-set-scraper

A Python toolchain for scraping recent RetroAchievements game claims, extracting ROM metadata, and searching for downloadable ROMs from public sources.

## Features

- Fetches the most recent game claims from the RetroAchievements API.
- Extracts game and console information, and retrieves ROM hash/title data.
- Searches for ROM download links from curated sources.
- Downloads ROMs with progress indication.
- Modular code with unit tests.

## Project Structure

```
├── make_request.py         # Fetches recent claims from the API
├── read_from_json.py       # Processes claim data and fetches ROM hashes/titles
├── rom_search.py           # Searches and downloads ROMs from sources
├── helpers.py              # Utility functions and ROM source definitions
├── data/                   # Stores intermediate and output JSON files
├── roms/                   # Downloaded ROM files
├── tests/                  # Unit tests
├── .env                    # API key configuration
├── requirements.txt        # Python dependencies
```

## Setup

1. **Clone the repository**
   ```sh
   git clone <repo-url>
   cd RA-set-scraper
   ```

2. **Install dependencies**
   It is recommended to use a virtual environment:
   ```sh
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Add your API Key**
   Create a .env file in the root directory with your RetroAchievements API key:
   ```
   API_KEY = "your_api_key_here"
   ```
4. **Add your API Key**
   Add your ROM output path to the .env:
   ```
   API_KEY = "your_api_key_here"
   ```

## Usage

1. **Fetch recent claims and write to JSON**
   ```sh
   python make_request.py
   ```
   This creates most_recent_claim.json. <br />
   **running this will prompt you for the number of roms you want to download.**


2. **Process claims and fetch ROM metadata**
   ```sh
   python read_from_json.py
   ```
   This creates rom_data.json.

3. **Search and download ROMs**
   ```sh
   python rom_search.py
   ```
   Downloaded ROMs will be saved in the roms directory.

## Testing

Run unit tests with:
```sh
python -m unittest discover tests
```

## Notes

- This tool is for educational and archival purposes. Respect copyright and intellectual property.
- The ROM sources are public archives; availability and legality may vary by region.

## License

MIT License (see `LICENSE` if present).

---

**Main scripts:**  
- make_request.py  
- read_from_json.py  
- rom_search.py  
- helpers.py  
- tests  
- requirements.txt