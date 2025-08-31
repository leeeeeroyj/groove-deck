#!/usr/bin/env python3
"""
Test script to verify audio commands can be imported.
"""
import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_audio_commands():
    """Test if audio commands can be imported."""
    try:
        print("🧪 Testing audio commands import...")
        
        # Test basic imports
        from src.config import Config
        print("✅ Config import successful")
        
        from src.commands.audio import AudioCommands
        print("✅ Audio commands import successful")
        
        print("\n🎉 Audio commands can be imported! The bot should work now.")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_audio_commands()
