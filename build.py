#!/usr/bin/env python3
"""
Build script for creating standalone executables of Alexa Silencer
"""

import subprocess
import sys
import os
import shutil
import platform

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"⏳ {description}...")
    try:
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

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("✅ PyInstaller is already installed")
        return True
    except ImportError:
        return run_command(f"{sys.executable} -m pip install pyinstaller", 
                          "Installing PyInstaller")

def build_executable():
    """Build the standalone executable"""
    os_name = platform.system().lower()
    
    # PyInstaller command
    cmd_parts = [
        "pyinstaller",
        "--onefile",
        "--noconsole" if os_name == "windows" else "--console",
        "--hidden-import=pygame",
        "--name=alexa-silencer",
        "alexa_silencer.py"
    ]
    
    command = " ".join(cmd_parts)
    
    return run_command(command, f"Building executable for {os_name}")

def create_distribution():
    """Create distribution folder with all necessary files"""
    os_name = platform.system().lower()
    dist_folder = f"alexa-silencer-{os_name}"
    
    # Create distribution folder
    if os.path.exists(dist_folder):
        shutil.rmtree(dist_folder)
    os.makedirs(dist_folder)
    
    # Copy executable
    if os_name == "windows":
        exe_name = "alexa-silencer.exe"
    else:
        exe_name = "alexa-silencer"
    
    exe_path = os.path.join("dist", exe_name)
    if os.path.exists(exe_path):
        shutil.copy2(exe_path, dist_folder)
        print(f"✅ Copied executable to {dist_folder}")
    else:
        print(f"❌ Executable not found at {exe_path}")
        return False
    
    # Copy documentation
    files_to_copy = ["README.md", "LICENSE", "requirements.txt"]
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, dist_folder)
            print(f"✅ Copied {file}")
    
    # Create simple run instructions
    if os_name == "windows":
        run_instructions = """# How to Run Alexa Silencer

1. Double-click on `alexa-silencer.exe`
2. The application will set up auto-startup and begin running in the background
3. That's it! Your Alexa device should now stay connected to Bluetooth

## To stop or remove:
- Open Task Manager and end the "alexa-silencer" process
- To remove auto-startup: Open Task Scheduler and delete the "AlexaSilencer" task

## Logs location:
%APPDATA%\\AlexaSilencer\\alexa_silencer.log
"""
    else:
        run_instructions = """# How to Run Alexa Silencer

1. Make the file executable: `chmod +x alexa-silencer`
2. Run it: `./alexa-silencer`
3. The application will set up auto-startup and begin running in the background
4. That's it! Your Alexa device should now stay connected to Bluetooth

## To stop or remove:
- To stop: `systemctl --user stop alexa-silencer`
- To remove auto-startup: `systemctl --user disable alexa-silencer`

## Logs location:
~/.alexa_silencer/alexa_silencer.log
"""
    
    with open(os.path.join(dist_folder, "RUN_INSTRUCTIONS.md"), "w") as f:
        f.write(run_instructions)
    
    print(f"✅ Created distribution folder: {dist_folder}")
    return True

def main():
    """Main build process"""
    print("🔨 Alexa Silencer Build Script")
    print("=" * 50)
    print()
    
    # Install PyInstaller
    if not install_pyinstaller():
        print("❌ Build failed during PyInstaller installation")
        return
    
    print()
    
    # Build executable
    if not build_executable():
        print("❌ Build failed during executable creation")
        return
    
    print()
    
    # Create distribution
    if create_distribution():
        print()
        print("🎉 Build Complete!")
        print()
        print("The standalone executable has been created and packaged for distribution.")
        print(f"Check the 'alexa-silencer-{platform.system().lower()}' folder for the complete package.")
    else:
        print("❌ Build failed during distribution creation")

if __name__ == "__main__":
    main()
