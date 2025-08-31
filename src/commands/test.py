"""
Test command to verify the bot is working.
"""
import discord
from discord import app_commands
from discord.ext import commands

class TestCommand(commands.Cog):
    """Simple test command to verify bot functionality."""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @app_commands.command(name="ping", description="Test if the bot is responding")
    async def ping(self, interaction: discord.Interaction):
        """Simple ping command to test bot response."""
        await interaction.response.send_message("🏓 Pong! Bot is working!")
        
    @app_commands.command(name="test", description="Test command for debugging")
    async def test(self, interaction: discord.Interaction):
        """Test command that shows bot information."""
        embed = discord.Embed(
            title="🤖 Bot Test",
            description="Bot is working correctly!",
            color=discord.Color.green()
        )
        embed.add_field(name="Channel ID", value=str(interaction.channel_id), inline=True)
        embed.add_field(name="Guild ID", value=str(interaction.guild_id), inline=True)
        embed.add_field(name="User ID", value=str(interaction.user.id), inline=True)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    """Set up the test command cog."""
    await bot.add_cog(TestCommand(bot))
