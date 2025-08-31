"""
Audio configuration presets for different quality levels.
"""
from typing import Dict, Any

class AudioConfig:
    """Audio configuration presets for different quality levels."""
    
    # High Quality Preset (Best audio, higher bandwidth)
    HIGH_QUALITY = {
        'ffmpeg_options': '-vn -b:a 160k -ar 48000 -ac 2 -f opus',
        'yt_dlp_format': 'bestaudio[ext=m4a]/bestaudio/best',
        'audio_format': 'm4a',
        'bitrate': '160k',
        'sample_rate': '48000'
    }
    
    # Balanced Quality Preset (Good audio, moderate bandwidth)
    BALANCED_QUALITY = {
        'ffmpeg_options': '-vn -b:a 128k -ar 48000 -ac 2 -f opus',
        'yt_dlp_format': 'bestaudio[ext=m4a]/bestaudio/best',
        'audio_format': 'm4a',
        'bitrate': '128k',
        'sample_rate': '48000'
    }
    
    # Low Bandwidth Preset (Lower quality, minimal bandwidth)
    LOW_BANDWIDTH = {
        'ffmpeg_options': '-vn -b:a 96k -ar 48000 -ac 2 -f opus',
        'yt_dlp_format': 'bestaudio/best',
        'audio_format': 'mp3',
        'bitrate': '96k',
        'sample_rate': '48000'
    }
    
    # Discord Optimized Preset (Optimized for Discord's limitations)
    DISCORD_OPTIMIZED = {
        'ffmpeg_options': '-vn -b:a 128k -ar 48000 -ac 2 -f opus -af "volume=1.0,highpass=f=200,lowpass=f=3000"',
        'yt_dlp_format': 'bestaudio[ext=m4a]/bestaudio/best',
        'audio_format': 'm4a',
        'bitrate': '128k',
        'sample_rate': '48000'
    }
    
    @classmethod
    def get_preset(cls, preset_name: str = 'balanced') -> Dict[str, Any]:
        """Get audio configuration preset by name."""
        presets = {
            'high': cls.HIGH_QUALITY,
            'balanced': cls.BALANCED_QUALITY,
            'low': cls.LOW_BANDWIDTH,
            'discord': cls.DISCORD_OPTIMIZED
        }
        return presets.get(preset_name.lower(), cls.BALANCED_QUALITY)
    
    @classmethod
    def list_presets(cls) -> Dict[str, str]:
        """List available audio presets with descriptions."""
        return {
            'high': 'High Quality - Best audio, higher bandwidth usage',
            'balanced': 'Balanced - Good audio, moderate bandwidth (default)',
            'low': 'Low Bandwidth - Lower quality, minimal bandwidth',
            'discord': 'Discord Optimized - Enhanced for Discord voice channels'
        }

# Default audio configuration
DEFAULT_AUDIO_CONFIG = AudioConfig.BALANCED_QUALITY
