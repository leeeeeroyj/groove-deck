#!/usr/bin/env python3
"""
Main entry point for Groove Deck Discord music bot.
"""
import asyncio
import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.bot import main

if __name__ == "__main__":
    asyncio.run(main())
