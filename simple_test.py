#!/usr/bin/env python3
"""
Simple import test for Groove Deck.
"""
import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

try:
    print("🧪 Testing basic imports...")
    
    # Test main config
    from src.config import Config
    print("✅ Main config import successful")
    
    # Test audio config
    from src.audio_config.audio_config import AudioConfig
    print("✅ Audio config import successful")
    
    print("\n🎉 All imports working! You can now run the bot.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print(f"Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
