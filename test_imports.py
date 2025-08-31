#!/usr/bin/env python3
"""
Test script to verify all imports work correctly.
"""
import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_imports():
    """Test all the main imports."""
    try:
        print("🧪 Testing imports...")
        
        # Test config import
        print("📁 Testing config import...")
        from src.config import Config
        print("✅ Config import successful")
        
        # Test logger import
        print("📝 Testing logger import...")
        from src.logger import logger
        print("✅ Logger import successful")
        
        # Test audio config import
        print("🎵 Testing audio config import...")
        from src.audio_config.audio_config import AudioConfig
        print("✅ Audio config import successful")
        
        # Test services import
        print("🔧 Testing services import...")
        from src.services.audio_player import audio_manager
        print("✅ Audio player import successful")
        
        from src.services.youtube_service import youtube_service
        print("✅ YouTube service import successful")
        
        print("\n🎉 All imports successful! The bot should work now.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_imports()
