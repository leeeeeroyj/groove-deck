"""
Main bot entry point for Groove Deck Discord music bot.
"""
import discord
from discord.ext import commands
import asyncio
import logging
import sys
import os

from src.config import Config
from src.logger import logger

class GrooveDeckBot(commands.Bot):
    """Main bot class for Groove Deck."""
    
    def __init__(self):
        # Set up intents - only use necessary non-privileged intents
        intents = discord.Intents.default()
        # Note: message_content and voice_states are privileged intents
        # that must be enabled in Discord Developer Portal under Bot > Privileged Gateway Intents
        intents.message_content = True
        intents.voice_states = True
        
        # Initialize bot with intents
        super().__init__(
            command_prefix=Config.BOT_PREFIX,
            intents=intents,
            help_command=None  # Disable default help command
        )
        
    async def setup_hook(self):
        """Set up the bot when it starts up."""
        logger.info("Setting up Groove Deck bot...")
        
        # Load command cogs
        try:
            await self.load_extension("src.commands.play")
            await self.load_extension("src.commands.queue")
            await self.load_extension("src.commands.test")
            await self.load_extension("src.commands.audio")
            logger.info("Successfully loaded all command cogs")
        except Exception as e:
            logger.error(f"Failed to load command cogs: {e}")
            raise
            
    async def on_ready(self):
        """Called when the bot is ready."""
        logger.info(f"Logged in as {self.user.name} (ID: {self.user.id})")
        logger.info(f"Bot is ready and serving {len(self.guilds)} guilds")
        
        # Sync slash commands
        try:
            synced = await self.tree.sync()
            logger.info(f"Synced {len(synced)} slash command(s)")
        except Exception as e:
            logger.error(f"Failed to sync slash commands: {e}")
            
    async def on_command_error(self, ctx, error):
        """Handle command errors."""
        if isinstance(error, commands.CommandNotFound):
            return  # Ignore command not found errors
            
        logger.error(f"Command error in {ctx.command}: {error}")
        
        # Send user-friendly error message
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission to use this command.")
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("❌ I don't have the required permissions to do that.")
        else:
            await ctx.send("❌ An error occurred while processing your command.")

async def main():
    """Main function to run the bot."""
    try:
        # Validate configuration
        if not Config.validate():
            logger.error("Invalid configuration. Please check your environment variables.")
            return
            
        # Create and run bot
        bot = GrooveDeckBot()
        
        # Run the bot
        async with bot:
            await bot.start(Config.DISCORD_TOKEN)
            
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise

if __name__ == "__main__":
    # Run the bot
    asyncio.run(main())
