#!/usr/bin/env python3
"""
Test script for Alexa Silencer
This script tests the core functionality without actually setting up auto-startup.
"""

import sys
import os
import tempfile
from pathlib import Path

# Add current directory to path for importing
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required modules can be imported"""
    try:
        import pygame
        print("✅ pygame imported successfully")
        
        import platform
        print("✅ platform module available")
        
        import logging
        print("✅ logging module available")
        
        import subprocess
        print("✅ subprocess module available")
        
        import threading
        print("✅ threading module available")
        
        import wave
        print("✅ wave module available")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_pygame_initialization():
    """Test pygame audio initialization"""
    try:
        import pygame
        
        # Initialize pygame mixer
        pygame.mixer.pre_init(frequency=22050, size=-16, channels=1, buffer=512)
        pygame.mixer.init()
        
        print("✅ pygame audio system initialized")
        
        # Test creating silent audio
        silence_duration = 0.01
        sample_rate = 22050
        samples = int(silence_duration * sample_rate)
        silent_audio = bytes(samples * 2)
        
        print("✅ Silent audio data created")
        
        # Test creating temporary WAV file
        temp_dir = Path(tempfile.gettempdir()) / "alexa_silencer_test"
        temp_dir.mkdir(exist_ok=True)
        test_file = temp_dir / "test_silence.wav"
        
        import wave
        with wave.open(str(test_file), 'w') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(silent_audio)
        
        print("✅ Silent WAV file created")
        
        # Test playing silent audio
        sound = pygame.mixer.Sound(str(test_file))
        sound.set_volume(0.0)
        sound.play()
        
        import time
        while pygame.mixer.get_busy():
            time.sleep(0.001)
        
        print("✅ Silent audio played successfully")
        
        # Cleanup
        pygame.mixer.quit()
        test_file.unlink(missing_ok=True)
        temp_dir.rmdir()
        
        print("✅ Cleanup completed")
        
        return True
        
    except Exception as e:
        print(f"❌ pygame test failed: {e}")
        return False

def test_os_detection():
    """Test OS detection and platform-specific features"""
    try:
        import platform
        
        os_type = platform.system().lower()
        print(f"✅ Detected OS: {os_type}")
        
        if os_type == "windows":
            print("✅ Windows-specific features will be used")
        elif os_type == "linux":
            print("✅ Linux-specific features will be used")
        else:
            print(f"⚠️  OS '{os_type}' may have limited support")
        
        return True
        
    except Exception as e:
        print(f"❌ OS detection failed: {e}")
        return False

def test_alexa_silencer_class():
    """Test the AlexaSilencer class initialization"""
    try:
        from alexa_silencer import AlexaSilencer
        
        # Create instance
        silencer = AlexaSilencer()
        print("✅ AlexaSilencer class instantiated")
        
        # Test app data directory creation
        app_dir = silencer.get_app_data_dir()
        print(f"✅ App data directory: {app_dir}")
        
        # Test pygame initialization
        if silencer.initialize_pygame():
            print("✅ AlexaSilencer pygame initialization successful")
            
            # Test silent audio creation and playback
            silencer.play_silent_audio()
            print("✅ Silent audio playback test successful")
            
            # Cleanup
            silencer.cleanup()
            print("✅ AlexaSilencer cleanup completed")
            
            return True
        else:
            print("❌ AlexaSilencer pygame initialization failed")
            return False
        
    except Exception as e:
        print(f"❌ AlexaSilencer test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Alexa Silencer Test Suite")
    print("=" * 50)
    print()
    
    tests = [
        ("Import Test", test_imports),
        ("pygame Test", test_pygame_initialization),
        ("OS Detection Test", test_os_detection),
        ("AlexaSilencer Class Test", test_alexa_silencer_class),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"🔍 Running {test_name}...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} passed")
            else:
                print(f"❌ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
        
        print()
    
    print("📊 Test Results")
    print("-" * 20)
    print(f"Passed: {passed}/{total}")
    print(f"Failed: {total - passed}/{total}")
    
    if passed == total:
        print()
        print("🎉 All tests passed! Alexa Silencer is ready to use.")
        print()
        print("To run the application:")
        print("  python alexa_silencer.py")
        print()
        print("Or use the setup script:")
        print("  python setup.py")
    else:
        print()
        print("❌ Some tests failed. Please check your environment and dependencies.")
        print()
        print("Try running:")
        print("  pip install -r requirements.txt")

if __name__ == "__main__":
    main()
