#!/usr/bin/env python3
"""
Alexa Silencer - A cross-platform background application that prevents Alexa devices 
from automatically disconnecting from Bluetooth by playing silent audio at regular intervals.

Author: 0x-Decrypt
License: MIT
GitHub: https://github.com/0x-Decrypt/alexa-silencer
"""

import os
import sys
import time
import logging
import platform
import subprocess
import threading
from pathlib import Path
import pygame
import tempfile
import signal

class AlexaSilencer:
    def __init__(self):
        self.running = False
        self.interval = 300  # 5 minutes in seconds
        self.os_type = platform.system().lower()
        self.setup_logging()
        
    def setup_logging(self):
        """Set up logging to file only (no console output)"""
        log_dir = self.get_app_data_dir()
        log_file = log_dir / "alexa_silencer.log"
        
        # Ensure log directory exists
        log_dir.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, mode='a'),
            ]
        )
        
        # Remove any console handlers
        for handler in logging.root.handlers[:]:
            if isinstance(handler, logging.StreamHandler) and handler.stream == sys.stdout:
                logging.root.removeHandler(handler)
        
        self.logger = logging.getLogger(__name__)
        
    def get_app_data_dir(self):
        """Get appropriate application data directory for the OS"""
        if self.os_type == "windows":
            app_data = os.getenv('APPDATA', os.path.expanduser('~'))
            return Path(app_data) / "AlexaSilencer"
        else:  # Linux and other Unix-like systems
            return Path.home() / ".alexa_silencer"
    
    def initialize_pygame(self):
        """Initialize pygame audio system silently"""
        try:
            # Initialize pygame mixer with minimal settings
            pygame.mixer.pre_init(frequency=22050, size=-16, channels=1, buffer=512)
            pygame.mixer.init()
            
            # Generate a very short silent audio clip (10ms of silence)
            silence_duration = 0.01  # 10 milliseconds
            sample_rate = 22050
            samples = int(silence_duration * sample_rate)
            
            # Create silent audio data (zeros) - using pure Python instead of numpy
            silent_audio = bytes(samples * 2)  # 2 bytes per sample for 16-bit audio
            
            # Create a temporary WAV file with silent audio
            self.temp_dir = Path(tempfile.gettempdir()) / "alexa_silencer"
            self.temp_dir.mkdir(exist_ok=True)
            self.silent_file = self.temp_dir / "silence.wav"
            
            # Write silent WAV file
            import wave
            with wave.open(str(self.silent_file), 'w') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(silent_audio)
            
            self.logger.info("Pygame audio system initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize pygame: {e}")
            return False
    
    def play_silent_audio(self):
        """Play silent audio to maintain Bluetooth connection"""
        try:
            # Load and play the silent audio file
            sound = pygame.mixer.Sound(str(self.silent_file))
            sound.set_volume(0.0)  # Ensure volume is at 0
            sound.play()
            
            # Wait for playback to complete
            while pygame.mixer.get_busy():
                time.sleep(0.001)
            
            self.logger.info("Silent audio played successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to play silent audio: {e}")
    
    def setup_windows_startup(self):
        """Configure auto-startup on Windows using Task Scheduler"""
        try:
            import winreg
            
            # Get current script path
            script_path = os.path.abspath(__file__)
            python_exe = sys.executable
            
            # Create a batch file to run the script silently
            batch_content = f'''@echo off
cd /d "{os.path.dirname(script_path)}"
"{python_exe}" "{script_path}" --daemon > nul 2>&1
'''
            
            app_dir = self.get_app_data_dir()
            app_dir.mkdir(parents=True, exist_ok=True)
            batch_file = app_dir / "alexa_silencer_startup.bat"
            
            with open(batch_file, 'w') as f:
                f.write(batch_content)
            
            # Create scheduled task using schtasks command
            task_name = "AlexaSilencer"
            cmd = [
                'schtasks', '/create', '/tn', task_name,
                '/tr', str(batch_file),
                '/sc', 'onlogon',
                '/rl', 'highest',
                '/f'  # Force overwrite if exists
            ]
            
            # Run with no window
            result = subprocess.run(cmd, capture_output=True, text=True, 
                                  creationflags=subprocess.CREATE_NO_WINDOW)
            
            if result.returncode == 0:
                self.logger.info("Windows startup configured successfully")
                return True
            else:
                self.logger.error(f"Failed to create scheduled task: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to setup Windows startup: {e}")
            return False
    
    def setup_linux_startup(self):
        """Configure auto-startup on Linux using systemd user service"""
        try:
            # Get current script path
            script_path = os.path.abspath(__file__)
            python_exe = sys.executable
            
            # Create systemd user service
            service_content = f"""[Unit]
Description=Alexa Silencer - Prevent Alexa Bluetooth disconnection
After=graphical-session.target

[Service]
Type=simple
ExecStart={python_exe} {script_path} --daemon
Restart=always
RestartSec=10
StandardOutput=null
StandardError=null

[Install]
WantedBy=default.target
"""
            
            # Create systemd user directory
            systemd_dir = Path.home() / ".config" / "systemd" / "user"
            systemd_dir.mkdir(parents=True, exist_ok=True)
            
            service_file = systemd_dir / "alexa-silencer.service"
            
            with open(service_file, 'w') as f:
                f.write(service_content)
            
            # Enable and start the service
            commands = [
                ['systemctl', '--user', 'daemon-reload'],
                ['systemctl', '--user', 'enable', 'alexa-silencer.service'],
                ['systemctl', '--user', 'start', 'alexa-silencer.service']
            ]
            
            for cmd in commands:
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode != 0:
                    self.logger.error(f"Command failed: {' '.join(cmd)} - {result.stderr}")
                    return False
            
            self.logger.info("Linux startup configured successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to setup Linux startup: {e}")
            return False
    
    def setup_startup(self):
        """Configure auto-startup based on the operating system"""
        self.logger.info(f"Setting up auto-startup for {self.os_type}")
        
        if self.os_type == "windows":
            return self.setup_windows_startup()
        elif self.os_type == "linux":
            return self.setup_linux_startup()
        else:
            self.logger.warning(f"Unsupported OS for auto-startup: {self.os_type}")
            return False
    
    def run_daemon(self):
        """Run the main daemon loop"""
        self.logger.info("Starting Alexa Silencer daemon")
        
        if not self.initialize_pygame():
            self.logger.error("Failed to initialize audio system")
            return
        
        self.running = True
        
        try:
            while self.running:
                self.play_silent_audio()
                
                # Sleep for the interval (5 minutes)
                for _ in range(self.interval):
                    if not self.running:
                        break
                    time.sleep(1)
                    
        except KeyboardInterrupt:
            self.logger.info("Received interrupt signal")
        except Exception as e:
            self.logger.error(f"Daemon error: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        self.running = False
        
        try:
            pygame.mixer.quit()
            
            # Clean up temporary files
            if hasattr(self, 'temp_dir') and self.temp_dir.exists():
                import shutil
                shutil.rmtree(self.temp_dir, ignore_errors=True)
                
        except Exception as e:
            self.logger.error(f"Cleanup error: {e}")
        
        self.logger.info("Alexa Silencer stopped")
    
    def setup_and_run(self):
        """One-time setup and run"""
        self.logger.info("Alexa Silencer setup started")
        
        # Setup auto-startup
        if self.setup_startup():
            self.logger.info("Auto-startup configured successfully")
            print("Alexa Silencer has been configured to run automatically on startup.")
            print("The application is now running in the background.")
        else:
            self.logger.error("Failed to configure auto-startup")
            print("Warning: Auto-startup configuration failed. You may need to run this manually on each boot.")
        
        # Start the daemon
        self.run_daemon()


def hide_console_window():
    """Hide the console window on Windows"""
    if platform.system().lower() == "windows":
        try:
            import ctypes
            # Get the console window handle
            hwnd = ctypes.windll.kernel32.GetConsoleWindow()
            if hwnd != 0:
                # Hide the console window
                ctypes.windll.user32.ShowWindow(hwnd, 0)
        except Exception:
            pass  # Fail silently


# Global flag for graceful shutdown
shutdown_flag = threading.Event()

def signal_handler(signum, frame):
    """Handle SIGTERM and SIGINT for graceful shutdown"""
    print(f"Received signal {signum}, shutting down gracefully...")
    shutdown_flag.set()
    sys.exit(0)

def main():
    """Main entry point"""
    # Hide console window immediately
    hide_console_window()
    
    silencer = AlexaSilencer()
    
    # Set up signal handlers
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--daemon":
        # Running as daemon (from startup)
        silencer.run_daemon()
    else:
        # First-time setup and run
        silencer.setup_and_run()
    
    # In your main loop, check for shutdown_flag
    while not shutdown_flag.is_set():
        pass  # Replace with actual work if needed


if __name__ == "__main__":
    main()
