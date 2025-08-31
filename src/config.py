"""
Configuration management for Groove Deck Discord bot.
"""
import os
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the Discord bot."""
    
    # Discord Bot Token
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    if not DISCORD_TOKEN:
        raise ValueError("DISCORD_TOKEN environment variable is required")
    
    # Spotify API Configuration
    SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
    SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
    
    # Channel Whitelist
    ALLOWED_CHANNEL_IDS = [
        int(channel_id.strip()) 
        for channel_id in os.getenv('ALLOWED_CHANNEL_IDS', '').split(',')
        if channel_id.strip()
    ]
    
    # Bot Configuration
    BOT_PREFIX = os.getenv('BOT_PREFIX', '!')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that all required configuration is present."""
        if not cls.DISCORD_TOKEN:
            return False
        return True
