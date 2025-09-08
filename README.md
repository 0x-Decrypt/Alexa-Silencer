# Alexa Silencer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Cross Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey.svg)](https://github.com/0x-Decrypt/alexa-silencer)

A cross-platform background application that prevents Alexa devices from automatically disconnecting from Bluetooth by playing silent audio at regular intervals.

## 🎯 Purpose

Alexa devices often disconnect from Bluetooth when there's no audio activity, causing annoying "Now connected to DEVICE_NAME" messages when they reconnect. Alexa Silencer solves this by playing completely silent audio every 5 minutes to maintain the Bluetooth connection.

**Problem solved**: No more interruptions from Alexa reconnection announcements!

## ✨ Features

- **Cross-Platform**: Works on both Windows and Linux
- **Completely Invisible**: Runs entirely in the background with no visible interface
- **Auto-Startup**: Automatically configures itself to run on system startup
- **One-Time Setup**: Run once and forget - no manual configuration needed
- **Silent Operation**: Plays 0-volume audio that's completely inaudible
- **Minimal Dependencies**: Only requires pygame for audio handling
- **Open Source**: MIT licensed and ready for community contributions

## 🚀 Quick Start

### Method 1: Automated Setup (Recommended)

**Windows:**
1. Download or clone this repository
2. Double-click `setup.bat` 
3. Done! The application will install dependencies and configure auto-startup

**Linux:**
1. Download or clone this repository
2. Run `chmod +x setup.sh && ./setup.sh`
3. Done! The application will install dependencies and configure auto-startup

### Method 2: Manual Setup

**Prerequisites:**
- Python 3.6 or higher
- pip (Python package installer)

**Steps:**
1. **Clone or download this repository**
   ```bash
   git clone https://github.com/0x-Decrypt/alexa-silencer.git
   cd alexa-silencer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application (one-time setup)**
   ```bash
   python alexa_silencer.py
   ```

### Method 3: Standalone Executable

1. Download the latest release from the [Releases page](https://github.com/0x-Decrypt/alexa-silencer/releases)
2. Run the executable for your platform
3. No Python installation required!

**What happens after setup:**
- ✅ Application configures itself to run automatically on startup
- ✅ Starts running in the background immediately  
- ✅ Plays silent audio every 5 minutes to maintain Bluetooth connection
- ✅ Your Alexa device stays connected without announcements!

## 💻 Platform-Specific Details

### Windows
- Uses Windows Task Scheduler for auto-startup
- Creates a scheduled task that runs on user logon
- Runs completely hidden with no console window

### Linux
- Uses systemd user services for auto-startup
- Creates `~/.config/systemd/user/alexa-silencer.service`
- Runs as a background daemon service

## 📁 File Locations

### Windows
- Logs: `%APPDATA%\AlexaSilencer\alexa_silencer.log`
- Startup script: `%APPDATA%\AlexaSilencer\alexa_silencer_startup.bat`

### Linux
- Logs: `~/.alexa_silencer/alexa_silencer.log`
- Service file: `~/.config/systemd/user/alexa-silencer.service`

## 🔧 Configuration

The application requires no manual configuration. Key settings:

- **Audio Interval**: 5 minutes (300 seconds)
- **Audio Duration**: 10 milliseconds of silence
- **Volume Level**: 0 (completely silent)
- **Audio Format**: 22050 Hz, 16-bit, mono

## 🛠️ Troubleshooting

### Check if it's running

**Windows:**
```cmd
tasklist | findstr python
# or
schtasks /query /tn "AlexaSilencer"
```

**Linux:**
```bash
systemctl --user status alexa-silencer
# or
ps aux | grep alexa_silencer
```

### View logs

**Windows:**
```cmd
type "%APPDATA%\AlexaSilencer\alexa_silencer.log"
```

**Linux:**
```bash
cat ~/.alexa_silencer/alexa_silencer.log
```

### Manually stop the service

**Windows:**
```cmd
schtasks /end /tn "AlexaSilencer"
```

**Linux:**
```bash
systemctl --user stop alexa-silencer
```

### Remove auto-startup

**Windows:**
```cmd
schtasks /delete /tn "AlexaSilencer" /f
```

**Linux:**
```bash
systemctl --user disable alexa-silencer
systemctl --user stop alexa-silencer
rm ~/.config/systemd/user/alexa-silencer.service
```

### Common Issues

**"pygame not found" error:**
```bash
pip install pygame
```

**Permission denied (Windows):**
- Run Command Prompt as Administrator
- Try: `schtasks /create /tn "AlexaSilencer" /tr "path\to\script" /sc onlogon /ru "SYSTEM"`

**Service fails to start (Linux):**
```bash
systemctl --user daemon-reload
systemctl --user restart alexa-silencer
journalctl --user -u alexa-silencer -f
```

## 🏗️ Building Standalone Executable

To create a single executable file for distribution:

### Option 1: Use Build Script (Recommended)
```bash
python build.py
```

This creates a distribution folder with:
- Standalone executable
- Documentation
- Run instructions

### Option 2: Manual PyInstaller
1. **Install PyInstaller**
   ```bash
   pip install pyinstaller
   ```

2. **Build executable**
   
   **Windows:**
   ```bash
   pyinstaller --onefile --noconsole --hidden-import=pygame --name=alexa-silencer alexa_silencer.py
   ```
   
   **Linux:**
   ```bash
   pyinstaller --onefile --console --hidden-import=pygame --name=alexa-silencer alexa_silencer.py
   ```

The executable will be in the `dist/` folder.

### Distribution
The build script creates platform-specific folders:
- `releases/` - Contains the latest executable for easy access
- Platform-specific distribution folders are created during build but excluded from source control

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test on both Windows and Linux if possible
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This application is designed to maintain Bluetooth connections with Alexa devices. While it plays silent audio, it may still consume minimal system resources and network bandwidth. Use responsibly and in accordance with your device manufacturer's terms of service.

## 🙋‍♂️ Support

If you encounter any issues or have questions:

1. Check the [troubleshooting section](#-troubleshooting)
2. Review the log files for error messages
3. Check the [FAQ section](#-frequently-asked-questions) below
4. Open an issue on GitHub with detailed information about your problem

## ❓ Frequently Asked Questions

### Q: Will this work with other Bluetooth devices?
**A:** Yes! While designed for Alexa, it works with any Bluetooth device that disconnects due to audio inactivity.

### Q: Can I change the 5-minute interval?
**A:** Currently the interval is fixed at 5 minutes. You can modify the `interval` variable in `alexa_silencer.py` if needed.

### Q: Does this consume noticeable system resources?
**A:** No, it uses <10MB RAM and <1% CPU. The silent audio is only 10ms every 5 minutes.

### Q: Will I hear any sound?
**A:** Absolutely not! The audio is set to 0 volume and is completely silent.

### Q: Can I run multiple instances?
**A:** Not recommended. One instance is sufficient and multiple instances may conflict.

### Q: How do I update to a new version?
**A:** Download the latest version and run it. It will automatically reconfigure the startup settings.

### Q: Is this safe for my computer?
**A:** Yes! The code is open source, uses standard libraries, and only plays silent audio. No network access or system modifications beyond startup configuration.

### Q: What if I want to completely remove it?
**A:** Use the removal commands in the troubleshooting section, then delete the application folder.

## 📊 System Requirements

- **Operating System**: Windows 10+ or Linux (any modern distribution)
- **Python**: 3.6 or higher (not required for standalone executables)
- **Memory**: <10 MB RAM usage
- **CPU**: Minimal impact (<1% CPU usage)
- **Storage**: <5 MB total footprint
- **Audio**: Any audio system (no speakers required)

## 🔍 How It Works

1. **Detection**: Automatically detects your operating system
2. **Audio Generation**: Creates 10ms silent audio files using pygame
3. **Scheduling**: Plays silent audio every 5 minutes (300 seconds)
4. **Background Operation**: Runs completely hidden from user interface
5. **Startup Integration**: Configures automatic startup using:
   - Windows: Task Scheduler
   - Linux: systemd user services

## 📈 Project Status

- ✅ **Stable Release** - Production ready
- ✅ **Cross-Platform** - Windows & Linux tested
- ✅ **Zero Dependencies** - Standalone executables available
- ✅ **Open Source** - MIT licensed
- ✅ **Community Driven** - Contributions welcome

## 🏷️ Version History

See [Releases](https://github.com/0x-Decrypt/alexa-silencer/releases) for detailed changelog.

---

**Made with ❤️ by [0x-Decrypt](https://github.com/0x-Decrypt)**

**⭐ Star this repo if it helped you!**
