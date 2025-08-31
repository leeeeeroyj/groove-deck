"""
Logging configuration for Groove Deck Discord bot.
"""
import logging
import sys
from src.config import Config

def setup_logger(name: str = "groove_deck") -> logging.Logger:
    """Set up and configure the logger."""
    logger = logging.getLogger(name)
    
    # Set log level from config
    log_level = getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # Create console handler if none exists
    if not logger.handlers:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(console_handler)
    
    return logger

# Create default logger instance
logger = setup_logger()
