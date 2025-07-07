import os
import time
import re
import urllib.parse
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from PyQt5.QtCore import QThread, pyqtSignal

from core.api_client import RetroAchievementsAPI
from core.rom_sources import ROM_SOURCES
from utils.text_utils import clean_title, clean_filename


class ROMCollectorWorker(QThread):
    progress_update = pyqtSignal(str)
    progress_percent = pyqtSignal(int)
    download_progress = pyqtSignal(str, int, int)  # filename, current, total
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, num_roms, download_path, api_key, selected_consoles=None):
        super().__init__()
        self.num_roms = num_roms
        self.download_path = download_path
        self.api_key = api_key
        self.selected_consoles = selected_consoles or []
        self.api_client = RetroAchievementsAPI(api_key)
        
    def run(self):
        try:
            # Step 1: Make API request
            self.progress_update.emit("🔄 Fetching recent claims from RetroAchievements...")
            self.progress_percent.emit(10)
            
            game_data = self.api_client.get_recent_claims()
            
            # Step 2: Get top N recent games
            self.progress_update.emit(f"📋 Processing {self.num_roms} most recent claims...")
            self.progress_percent.emit(20)
            
            sorted_data = sorted(game_data, key=lambda entry: entry.get("DoneTime", ""), reverse=True)
            most_recent = sorted_data[:self.num_roms]
            
            # Step 3: Process game data
            self.progress_update.emit("🎮 Processing game information...")
            self.progress_percent.emit(30)
            
            game_dict = {'games': [], 'consoles': [], 'gameHashes': []}
            game_urls = []
            
            for game in most_recent:
                game_id = game['GameID']
                console_name = game['ConsoleName']
                
                # Filter by selected consoles if specified
                if self.selected_consoles and console_name not in self.selected_consoles:
                    continue
                    
                game_hash_url = f"https://retroachievements.org/API/API_GetGameHashes.php?i={game_id}&y={self.api_key}"
                game_dict['games'].append(game_id)
                game_dict['consoles'].append(console_name)
                game_dict['gameHashes'].append(game_hash_url)
                game_urls.append(game_hash_url)
                time.sleep(0.5)
            
            # Step 4: Get ROM titles
            self.progress_update.emit("🔍 Retrieving Game titles...")
            self.progress_percent.emit(50)
            
            game_title_list = []
            for i, (url, console) in enumerate(zip(game_urls, game_dict['consoles'])):
                try:
                    r = requests.get(url)
                    r.raise_for_status()
                    data = r.json()
                    
                    results = data.get('Results', [])
                    if not results:
                        game_title_list.append('Unknown')
                        continue
                    
                    clean_results = [res for res in results if not res.get('PatchUrl')]
                    if len(clean_results) == 0:
                        selected_result = results[0]
                    else:
                        selected_result = clean_results[0]
                    
                    raw_name = selected_result.get('Name', 'Unknown Title')
                    
                    if console == "Arcade":
                        filename = raw_name.split()[0]
                        rom_base_name = re.sub(r'\.[a-z0-9]+$', '', filename, flags=re.IGNORECASE)
                    else:
                        rom_base_name = clean_title(raw_name)
                    
                    game_title_list.append(rom_base_name.strip())
                    self.progress_update.emit(f"📝 Found: {rom_base_name.strip()} ({console})")
                    time.sleep(0.5)
                    
                except Exception as e:
                    self.progress_update.emit(f"❌ Error processing game: {e}")
                    game_title_list.append('Error')
            
            # Step 5: Search and download ROMs
            self.progress_update.emit("⬇️ Starting Game downloads...")
            self.progress_percent.emit(70)
            
            downloaded_count = 0
            for i, (title, console) in enumerate(zip(game_title_list, game_dict['consoles'])):
                if title in ['Unknown', 'Error']:
                    continue
                    
                success = self.find_and_download_rom(title, console)
                if success:
                    downloaded_count += 1
                
                progress = 70 + int((i / len(game_title_list)) * 25)
                self.progress_percent.emit(progress)
            
            self.progress_percent.emit(100)
            self.finished.emit(f"✅ Process completed! Downloaded {downloaded_count} Games")
            
        except Exception as e:
            self.error.emit(str(e))
    
    def find_and_download_rom(self, title, console):
        """Find and download a ROM from available sources"""
        source_urls = ROM_SOURCES.get(console)
        if not source_urls:
            self.progress_update.emit(f"⚠️ No Game source for console: {console}")
            return False
        
        if isinstance(source_urls, str):
            source_urls = [source_urls]
        
        self.progress_update.emit(f"🔍 Searching for: {title}")
        
        for url in source_urls:
            try:
                response = requests.get(url)
                response.raise_for_status()
                
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
                            
                            return self.download_rom(full_url, filename, console)
                            
                time.sleep(0.5)
                
            except Exception as e:
                self.progress_update.emit(f"❌ Error accessing {url}: {e}")
        
        self.progress_update.emit(f"❌ No match found for {title}")
        return False
    
    def download_rom(self, full_url, filename, console):
        """Download a ROM file to the appropriate console directory"""
        try:
            self.progress_update.emit(f"⬇️ Starting download: {filename}")
            response = requests.get(full_url, stream=True)
            response.raise_for_status()
            
            console_dir = os.path.join(self.download_path, "Games", console)
            os.makedirs(console_dir, exist_ok=True)
            
            filepath = os.path.join(console_dir, filename)
            
            if os.path.exists(filepath):
                self.progress_update.emit(f"⚠️ Skipped (already exists): {filename}")
                return True
            
            # Get total file size
            total_size = int(response.headers.get('Content-Length', 0))
            downloaded = 0
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        # Emit download progress
                        if total_size > 0:
                            percent = int((downloaded / total_size) * 100)
                            self.download_progress.emit(filename, downloaded, total_size)
            
            self.progress_update.emit(f"✅ Downloaded: {filename}")
            return True
            
        except Exception as e:
            self.progress_update.emit(f"❌ Failed to download {filename}: {e}")
            return False