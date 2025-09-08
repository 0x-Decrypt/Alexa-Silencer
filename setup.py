#!/usr/bin/env python3
"""
Setup script for Alexa Silencer
This script helps users install dependencies and set up the application.
"""

import subprocess
import sys
import os
import platform

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"⏳ {description}...")
    try:
        if platform.system().lower() == "windows":
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
        else:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ {description} failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} failed: {e}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 6):
        print("❌ Python 3.6 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_dependencies():
    """Install required Python packages"""
    requirements_file = "requirements.txt"
    if not os.path.exists(requirements_file):
        print(f"❌ {requirements_file} not found")
        return False
    
    return run_command(f"{sys.executable} -m pip install -r {requirements_file}", 
                      "Installing dependencies")

def setup_alexa_silencer():
    """Run the Alexa Silencer setup"""
    script_path = "alexa_silencer.py"
    if not os.path.exists(script_path):
        print(f"❌ {script_path} not found")
        return False
    
    print("🚀 Starting Alexa Silencer setup...")
    print("   This will configure auto-startup and begin running the application.")
    print("   The application will run invisibly in the background.")
    
    try:
        # Run the main script
        if platform.system().lower() == "windows":
            subprocess.Popen([sys.executable, script_path], 
                           creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            subprocess.Popen([sys.executable, script_path], 
                           stdout=subprocess.DEVNULL, 
                           stderr=subprocess.DEVNULL)
        
        print("✅ Alexa Silencer has been started and configured for auto-startup")
        return True
        
    except Exception as e:
        print(f"❌ Failed to start Alexa Silencer: {e}")
        return False

def main():
    """Main setup process"""
    print("🔧 Alexa Silencer Setup")
    print("=" * 50)
    print()
    
    # Check Python version
    if not check_python_version():
        input("Press Enter to exit...")
        return
    
    print()
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Setup failed during dependency installation")
        input("Press Enter to exit...")
        return
    
    print()
    
    # Setup and run Alexa Silencer
    if setup_alexa_silencer():
        print()
        print("🎉 Setup Complete!")
        print()
        print("Alexa Silencer is now:")
        print("  • Running in the background")
        print("  • Configured to start automatically on boot")
        print("  • Playing silent audio every 5 minutes")
        print()
        print("Your Alexa device should now stay connected to Bluetooth!")
        print()
        print("Note: The application runs completely invisibly.")
        print("Check the logs if you need to troubleshoot:")
        
        if platform.system().lower() == "windows":
            print("  Windows: %APPDATA%\\AlexaSilencer\\alexa_silencer.log")
        else:
            print("  Linux: ~/.alexa_silencer/alexa_silencer.log")
    else:
        print("❌ Setup failed during Alexa Silencer configuration")
    
    print()
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
