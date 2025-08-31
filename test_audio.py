#!/usr/bin/env python3
"""
Audio quality test script for Groove Deck.
This script helps test different audio configurations without running the full bot.
"""
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.audio_config.audio_config import AudioConfig

def test_audio_configs():
    """Test and display all available audio configurations."""
    print("🎵 Groove Deck Audio Configuration Test")
    print("=" * 50)
    
    # List all presets
    presets = AudioConfig.list_presets()
    for name, description in presets.items():
        print(f"\n📻 {name.upper()} QUALITY:")
        print(f"   {description}")
        
        # Get the preset configuration
        config = AudioConfig.get_preset(name)
        print(f"   Bitrate: {config['bitrate']}")
        print(f"   Sample Rate: {config['sample_rate']} Hz")
        print(f"   Format: {config['audio_format'].upper()}")
        print(f"   FFmpeg Options: {config['ffmpeg_options']}")
    
    print("\n" + "=" * 50)
    print("💡 To use these in your bot:")
    print("   1. Restart your bot after making changes")
    print("   2. Use `/audio` to see current settings")
    print("   3. Use `/audio_quality:preset_name` to change quality")
    print("\n🎯 Recommended starting point: 'discord' preset")
    print("   This preset is optimized for Discord's voice limitations")

if __name__ == "__main__":
    test_audio_configs()
