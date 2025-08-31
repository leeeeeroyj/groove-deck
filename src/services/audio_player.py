"""
Audio player service for managing music queues and playback.
"""
import asyncio
import logging
from typing import List, Optional, Dict
from dataclasses import dataclass
from discord import VoiceChannel, VoiceClient, FFmpegPCMAudio
from discord.ext import commands
import yt_dlp

logger = logging.getLogger(__name__)

@dataclass
class Track:
    """Represents a music track."""
    title: str
    url: str
    duration: Optional[int] = None
    requester_id: Optional[int] = None

class AudioPlayer:
    """Manages audio playback and queue for a single guild."""
    
    def __init__(self, guild_id: int):
        self.guild_id = guild_id
        self.queue: List[Track] = []
        self.current_track: Optional[Track] = None
        self.voice_client: Optional[VoiceClient] = None
        self.is_playing = False
        self.loop = False
        
    def add_track(self, track: Track) -> None:
        """Add a track to the queue."""
        self.queue.append(track)
        logger.info(f"Added track '{track.title}' to queue for guild {self.guild_id}")
        
    def remove_track(self, position: int) -> Optional[Track]:
        """Remove a track from the queue by position."""
        if 0 <= position < len(self.queue):
            track = self.queue.pop(position)
            logger.info(f"Removed track '{track.title}' from position {position}")
            return track
        return None
        
    def move_track(self, from_pos: int, to_pos: int) -> bool:
        """Move a track from one position to another in the queue."""
        if (0 <= from_pos < len(self.queue) and 
            0 <= to_pos < len(self.queue) and 
            from_pos != to_pos):
            track = self.queue.pop(from_pos)
            self.queue.insert(to_pos, track)
            logger.info(f"Moved track '{track.title}' from position {from_pos} to {to_pos}")
            return True
        return False
        
    def skip_current(self) -> Optional[Track]:
        """Skip the current track and return the next one."""
        if self.current_track:
            logger.info(f"Skipped track '{self.current_track.title}'")
            
        if self.queue:
            self.current_track = self.queue.pop(0)
            return self.current_track
        else:
            self.current_track = None
            self.is_playing = False
            return None
            
    def stop_playback(self) -> None:
        """Stop playback and clear the queue."""
        self.queue.clear()
        self.current_track = None
        self.is_playing = False
        if self.voice_client:
            self.voice_client.stop()
        logger.info(f"Stopped playback for guild {self.guild_id}")
        
    def get_queue_info(self) -> Dict:
        """Get information about the current queue."""
        return {
            'current_track': self.current_track,
            'queue': self.queue,
            'is_playing': self.is_playing,
            'queue_length': len(self.queue)
        }

class AudioManager:
    """Manages audio players for multiple guilds."""
    
    def __init__(self):
        self.players: Dict[int, AudioPlayer] = {}
        
    def get_player(self, guild_id: int) -> AudioPlayer:
        """Get or create an audio player for a guild."""
        if guild_id not in self.players:
            self.players[guild_id] = AudioPlayer(guild_id)
        return self.players[guild_id]
        
    def remove_player(self, guild_id: int) -> None:
        """Remove an audio player for a guild."""
        if guild_id in self.players:
            player = self.players[guild_id]
            player.stop_playback()
            del self.players[guild_id]
            logger.info(f"Removed audio player for guild {guild_id}")

# Global audio manager instance
audio_manager = AudioManager()
