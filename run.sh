#!/bin/bash

# Groove Deck Discord Bot Startup Script

echo "🎵 Starting Groove Deck Discord Bot..."

# Check if conda is available
if command -v conda &> /dev/null; then
    echo "📦 Activating conda environment..."
    source $(conda info --base)/etc/profile.d/conda.sh
    conda activate groove-deck
else
    echo "⚠️  Conda not found. Make sure you have the correct Python environment activated."
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "Please copy env.example to .env and configure your Discord bot token."
    exit 1
fi

# Check if main.py exists
if [ ! -f main.py ]; then
    echo "❌ main.py not found!"
    echo "Please make sure you're in the correct directory."
    exit 1
fi

echo "🚀 Starting bot..."
python main.py
