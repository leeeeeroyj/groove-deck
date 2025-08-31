"""
Audio quality control commands for the music bot.
"""
import discord
from discord import app_commands
from discord.ext import commands
import logging

from src.config import Config

logger = logging.getLogger(__name__)

class AudioCommands(commands.Cog):
    """Handles audio quality control commands."""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @app_commands.command(name="audio", description="Show current audio settings and quality options")
    async def audio(self, interaction: discord.Interaction):
        """Display current audio configuration and available presets."""
        
        # Check if channel is whitelisted
        if interaction.channel_id not in Config.ALLOWED_CHANNEL_IDS:
            await interaction.response.send_message(
                "❌ This command is not allowed in this channel.", 
                ephemeral=True
            )
            return
            
        # Create embed showing current settings
        embed = discord.Embed(
            title="🎵 Audio Configuration",
            description="Current audio settings and available presets",
            color=discord.Color.blue()
        )
        
        # Current settings
        embed.add_field(
            name="⚙️ Current Settings",
            value="**Format:** MP3\n"
                  "**Sample Rate:** 48kHz\n"
                  "**Channels:** Stereo (2)\n"
                  "**Codec:** s16le (Discord compatible)",
            inline=True
        )
        
        # Available presets
        embed.add_field(
            name="🎚️ Audio Quality",
            value="**Current:** Discord Optimized\n"
                  "**Format:** MP3 (128k)\n"
                  "**Compatibility:** High",
            inline=True
        )
        
        embed.add_field(
            name="💡 Note",
            value="Audio is optimized for Discord voice channels.\n"
                  "Using MP3 format for maximum compatibility.",
            inline=False
        )
        
        await interaction.response.send_message(embed=embed)
        
    @app_commands.command(name="audio_quality", description="Show current audio quality information")
    async def audio_quality(self, interaction: discord.Interaction):
        """Show current audio quality information."""
        
        # Check if channel is whitelisted
        if interaction.channel_id not in Config.ALLOWED_CHANNEL_IDS:
            await interaction.response.send_message(
                "❌ This command is not allowed in this channel.", 
                ephemeral=True
            )
            return
            
        # Create confirmation embed
        embed = discord.Embed(
            title="🎵 Audio Quality Info",
            description="Current audio configuration",
            color=discord.Color.green()
        )
        
        embed.add_field(
            name="Current Settings",
            value="**Format:** MP3\n"
                  "**Bitrate:** 128k\n"
                  "**Sample Rate:** 48kHz\n"
                  "**Channels:** Stereo",
            inline=True
        )
        
        embed.add_field(
            name="Discord Compatibility",
            value="**Status:** ✅ Optimized\n"
                  "**Format:** ✅ Compatible\n"
                  "**Quality:** ✅ High",
            inline=True
        )
        
        embed.add_field(
            name="Note",
            value="Audio is configured for maximum Discord compatibility.\n"
                  "This should eliminate static/white noise issues.",
            inline=False
        )
        
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    """Set up the audio commands cog."""
    await bot.add_cog(AudioCommands(bot))
