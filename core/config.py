"""
Configuration management for RetroAchievements ROM Collector
"""

import os
from pathlib import Path
from dotenv import load_dotenv


class Config:
    """Application configuration manager"""
    
    def __init__(self):
        self.load_config()
    
    def load_config(self):
        """Load configuration from environment variables and .env file"""
        # Load from .env file if it exists
        env_path = Path('.env')
        if env_path.exists():
            load_dotenv(env_path)
        
        # Set default values
        self.api_key = os.environ.get('API_KEY', '')
        self.download_path = os.environ.get('DIRECTORY_PATH', str(Path.home()))
        self.api_base_url = "https://retroachievements.org/API"
        self.default_rom_count = 10
        self.max_rom_count = 100
        self.request_delay = 0.5  # seconds between API requests
        self.download_chunk_size = 8192
    
    def save_config(self, api_key=None, download_path=None):
        """Save configuration to .env file"""
        if api_key is not None:
            self.api_key = api_key
        if download_path is not None:
            self.download_path = download_path
        
        env_content = f"API_KEY={self.api_key}\nDIRECTORY_PATH={self.download_path}\n"
        with open('.env', 'w') as f:
            f.write(env_content)
    
    def get_api_key(self):
        """Get the API key"""
        return self.api_key
    
    def get_api_url(self, endpoint):
        """Get full API URL for a given endpoint"""
        return f"{self.api_base_url}/{endpoint}"
    
    def get_download_path(self):
        """Get the download path"""
        return self.download_path
    
    def is_valid(self):
        """Check if configuration is valid"""
        return bool(self.api_key and self.download_path)


# Global configuration instance
config = Config()