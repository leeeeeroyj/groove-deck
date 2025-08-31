"""
Queue management commands for the music bot.
"""
import discord
from discord import app_commands
from discord.ext import commands
import logging
from typing import Optional

from src.services.audio_player import audio_manager
from src.config import Config

logger = logging.getLogger(__name__)

class QueueCommands(commands.Cog):
    """Handles queue management commands."""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @app_commands.command(name="queue", description="Show the current music queue")
    async def queue(self, interaction: discord.Interaction):
        """Display the current music queue."""
        
        # Check if channel is whitelisted
        if interaction.channel_id not in Config.ALLOWED_CHANNEL_IDS:
            await interaction.response.send_message(
                "❌ This command is not allowed in this channel.", 
                ephemeral=True
            )
            return
            
        player = audio_manager.get_player(interaction.guild_id)
        queue_info = player.get_queue_info()
        
        if not queue_info['current_track'] and not queue_info['queue']:
            await interaction.response.send_message("🎵 No music is currently playing or queued.")
            return
            
        # Create embed for queue display
        embed = discord.Embed(
            title="🎵 Music Queue",
            color=discord.Color.blue()
        )
        
        # Current track
        if queue_info['current_track']:
            current = queue_info['current_track']
            embed.add_field(
                name="🎶 Now Playing",
                value=f"**{current.title}**",
                inline=False
            )
            
        # Queue
        if queue_info['queue']:
            queue_text = ""
            for i, track in enumerate(queue_info['queue'], 1):
                queue_text += f"**{i}.** {track.title}\n"
                
            embed.add_field(
                name=f"📋 Up Next ({len(queue_info['queue'])} tracks)",
                value=queue_text[:1024],  # Discord embed field limit
                inline=False
            )
            
        await interaction.response.send_message(embed=embed)
        
    @app_commands.command(name="skip", description="Skip the current song")
    async def skip(self, interaction: discord.Interaction):
        """Skip the current song and play the next one."""
        
        # Check if channel is whitelisted
        if interaction.channel_id not in Config.ALLOWED_CHANNEL_IDS:
            await interaction.response.send_message(
                "❌ This command is not allowed in this channel.", 
                ephemeral=True
            )
            return
            
        player = audio_manager.get_player(interaction.guild_id)
        
        if not player.is_playing or not player.current_track:
            await interaction.response.send_message("❌ No music is currently playing.")
            return
            
        # Skip current track
        next_track = player.skip_current()
        
        if next_track:
            await interaction.response.send_message(
                f"⏭️ Skipped! Now playing: **{next_track.title}**"
            )
        else:
            await interaction.response.send_message("⏹️ Stopped playback - no more tracks in queue.")
            
    @app_commands.command(name="stop", description="Stop playback and clear the queue")
    async def stop(self, interaction: discord.Interaction):
        """Stop playback and clear the queue."""
        
        # Check if channel is whitelisted
        if interaction.channel_id not in Config.ALLOWED_CHANNEL_IDS:
            await interaction.response.send_message(
                "❌ This command is not allowed in this channel.", 
                ephemeral=True
            )
            return
            
        player = audio_manager.get_player(interaction.guild_id)
        
        if not player.is_playing and not player.queue:
            await interaction.response.send_message("❌ No music is currently playing or queued.")
            return
            
        # Stop playback
        player.stop_playback()
        
        await interaction.response.send_message("⏹️ Stopped playback and cleared the queue.")
        
    @app_commands.command(name="remove", description="Remove a song from the queue")
    @app_commands.describe(position="Position of the song to remove (1, 2, 3, etc.)")
    async def remove(self, interaction: discord.Interaction, position: int):
        """Remove a song from the queue by position."""
        
        # Check if channel is whitelisted
        if interaction.channel_id not in Config.ALLOWED_CHANNEL_IDS:
            await interaction.response.send_message(
                "❌ This command is not allowed in this channel.", 
                ephemeral=True
            )
            return
            
        player = audio_manager.get_player(interaction.guild_id)
        
        if not player.queue:
            await interaction.response.send_message("❌ The queue is empty.")
            return
            
        # Convert to 0-based index
        queue_position = position - 1
        
        if queue_position < 0 or queue_position >= len(player.queue):
            await interaction.response.send_message(
                f"❌ Invalid position. Queue has {len(player.queue)} tracks."
            )
            return
            
        # Remove track
        removed_track = player.remove_track(queue_position)
        
        if removed_track:
            await interaction.response.send_message(
                f"🗑️ Removed **{removed_track.title}** from the queue."
            )
        else:
            await interaction.response.send_message("❌ Failed to remove track.")
            
    @app_commands.command(name="move", description="Move a song to a different position in the queue")
    @app_commands.describe(
        from_position="Current position of the song (1, 2, 3, etc.)",
        to_position="New position for the song (1, 2, 3, etc.)"
    )
    async def move(self, interaction: discord.Interaction, from_position: int, to_position: int):
        """Move a song from one position to another in the queue."""
        
        # Check if channel is whitelisted
        if interaction.channel_id not in Config.ALLOWED_CHANNEL_IDS:
            await interaction.response.send_message(
                "❌ This command is not allowed in this channel.", 
                ephemeral=True
            )
            return
            
        player = audio_manager.get_player(interaction.guild_id)
        
        if not player.queue:
            await interaction.response.send_message("❌ The queue is empty.")
            return
            
        # Convert to 0-based indices
        from_pos = from_position - 1
        to_pos = to_position - 1
        
        if (from_pos < 0 or from_pos >= len(player.queue) or 
            to_pos < 0 or to_pos >= len(player.queue)):
            await interaction.response.send_message(
                f"❌ Invalid positions. Queue has {len(player.queue)} tracks."
            )
            return
            
        if from_pos == to_pos:
            await interaction.response.send_message("❌ Cannot move to the same position.")
            return
            
        # Move track
        success = player.move_track(from_pos, to_pos)
        
        if success:
            moved_track = player.queue[to_pos]
            await interaction.response.send_message(
                f"🔄 Moved **{moved_track.title}** from position {from_position} to {to_position}."
            )
        else:
            await interaction.response.send_message("❌ Failed to move track.")

async def setup(bot: commands.Bot):
    """Set up the queue commands cog."""
    await bot.add_cog(QueueCommands(bot))
