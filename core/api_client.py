"""
RetroAchievements API client
"""

import requests
import time
from typing import Dict, List, Optional
from .config import config


class RetroAchievementsAPI:
    """Client for RetroAchievements API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'RetroAchievements-ROM-Collector/1.0'
        })
    
    def get_recent_claims(self) -> List[Dict]:
        """Get recent achievement claims"""
        url = config.get_api_url(f"API_GetClaims.php?k=1&y={self.api_key}")
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch claims: {e}")
    
    def get_game_hashes(self, game_id: int) -> Dict:
        """Get game hashes for a specific game ID"""
        url = config.get_api_url(f"API_GetGameHashes.php?i={game_id}&y={self.api_key}")
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch game hashes for game {game_id}: {e}")
    
    def get_game_info(self, game_id: int) -> Dict:
        """Get detailed game information"""
        url = config.get_api_url(f"API_GetGame.php?i={game_id}&y={self.api_key}")
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch game info for game {game_id}: {e}")
    
    def rate_limit_delay(self):
        """Apply rate limiting delay"""
        time.sleep(config.request_delay)