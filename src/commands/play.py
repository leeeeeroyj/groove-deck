"""
Play command for adding music to the queue and starting playback.
"""
import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import logging
from typing import Optional

from src.services.audio_player import audio_manager, Track
from src.services.youtube_service import youtube_service
from src.config import Config

logger = logging.getLogger(__name__)

class PlayCommand(commands.Cog):
    """Handles music playback commands."""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @app_commands.command(name="play", description="Play a song from YouTube")
    @app_commands.describe(query="Song name, artist, or YouTube URL")
    async def play(self, interaction: discord.Interaction, query: str):
        """Play a song from YouTube."""
        
        # Check if channel is whitelisted
        if interaction.channel_id not in Config.ALLOWED_CHANNEL_IDS:
            await interaction.response.send_message(
                "❌ This command is not allowed in this channel.", 
                ephemeral=True
            )
            return
            
        # Check if user is in a voice channel
        if not interaction.user.voice or not interaction.user.voice.channel:
            await interaction.response.send_message(
                "❌ You must be in a voice channel to use this command.", 
                ephemeral=True
            )
            return
            
        await interaction.response.defer()
        
        try:
            # Search for the video
            video_info = youtube_service.search_video(query)
            
            if not video_info:
                await interaction.followup.send(
                    "❌ Could not find any videos matching your query."
                )
                return
                
            # Create track object
            track = Track(
                title=video_info['title'],
                url=video_info['url'],
                duration=video_info.get('duration'),
                requester_id=interaction.user.id
            )
            
            # Get or create audio player for this guild
            player = audio_manager.get_player(interaction.guild_id)
            
            # Add track to queue
            player.add_track(track)
            
            # If not currently playing, start playback
            if not player.is_playing:
                await self._start_playback(interaction, player, track)
            else:
                await interaction.followup.send(
                    f"🎵 Added **{track.title}** to the queue!"
                )
                
        except Exception as e:
            logger.error(f"Error in play command: {e}")
            await interaction.followup.send(
                "❌ An error occurred while processing your request."
            )
            
    async def _start_playback(self, interaction: discord.Interaction, player: 'AudioPlayer', track: Track):
        """Start playback of a track."""
        try:
            voice_channel = interaction.user.voice.channel
            
            # Connect to voice channel
            voice_client = await voice_channel.connect()
            player.voice_client = voice_client
            player.current_track = track
            player.is_playing = True
            
            # Get audio URL and start playing
            audio_url = youtube_service.get_audio_url(track.url)
            
            if audio_url:
                # Create audio source
                audio_source = discord.FFmpegPCMAudio(
                    audio_url,
                    options='-vn -b:a 192k'
                )
                
                # Play audio
                voice_client.play(audio_source)
                
                await interaction.followup.send(
                    f"🎵 Now playing: **{track.title}**"
                )
                
                # Set up callback for when audio finishes
                def on_finish(error):
                    if error:
                        logger.error(f"Audio playback error: {error}")
                    
                    # Play next track in queue
                    asyncio.create_task(self._play_next(interaction.guild_id))
                
                voice_client.source = audio_source
                voice_client.source.callback = on_finish
                
            else:
                await interaction.followup.send(
                    "❌ Could not extract audio from the video."
                )
                player.stop_playback()
                
        except Exception as e:
            logger.error(f"Error starting playback: {e}")
            await interaction.followup.send(
                "❌ Failed to start playback. Please try again."
            )
            player.stop_playback()
            
    async def _play_next(self, guild_id: int):
        """Play the next track in the queue."""
        player = audio_manager.get_player(guild_id)
        
        if player.queue:
            next_track = player.queue.pop(0)
            player.current_track = next_track
            
            # Get audio URL and start playing
            audio_url = youtube_service.get_audio_url(next_track.url)
            
            if audio_url and player.voice_client:
                audio_source = discord.FFmpegPCMAudio(
                    audio_url,
                    options='-vn -b:a 192k'
                )
                
                player.voice_client.play(audio_source)
                
                # Set up callback for when audio finishes
                def on_finish(error):
                    if error:
                        logger.error(f"Audio playback error: {error}")
                    
                    # Play next track in queue
                    asyncio.create_task(self._play_next(guild_id))
                
                player.voice_client.source = audio_source
                player.voice_client.source.callback = on_finish
                
        else:
            # No more tracks in queue
            player.is_playing = False
            player.current_track = None
            
            # Disconnect after a delay
            if player.voice_client:
                await asyncio.sleep(10)  # Wait 10 seconds
                if player.voice_client and not player.is_playing:
                    await player.voice_client.disconnect()

async def setup(bot: commands.Bot):
    """Set up the play command cog."""
    await bot.add_cog(PlayCommand(bot))
