# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-08

### Added
- Initial release of Alexa Silencer
- Cross-platform support (Windows and Linux)
- Completely invisible background operation
- Automatic startup configuration
- Silent audio playback every 5 minutes to maintain Bluetooth connection
- One-time setup process
- Comprehensive logging system
- MIT license
- Multiple installation methods (Python script, standalone executable)
- Setup helpers for Windows (`setup.bat`) and Linux (`setup.sh`)
- Build script for creating standalone executables
- Comprehensive test suite
- Documentation for users and contributors
- GitHub Actions ready project structure

### Features
- **Silent Operation**: Plays 0-volume audio that's completely inaudible
- **Auto-Startup**: Configures itself to run on system startup automatically
- **Cross-Platform**: Works on both Windows (Task Scheduler) and Linux (systemd)
- **Minimal Dependencies**: Only requires pygame for audio handling
- **Background Service**: Runs entirely hidden with no visible interface
- **Easy Setup**: Run once and forget - no manual configuration needed

### Technical Details
- Python 3.6+ compatibility
- pygame-based audio system
- Platform-specific startup configuration
- Comprehensive error handling and logging
- Resource cleanup and management
- Temporary file handling for silent audio generation

[1.0.0]: https://github.com/0x-Decrypt/alexa-silencer/releases/tag/v1.0.0
