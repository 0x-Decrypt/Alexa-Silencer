# Contributing to Alexa Silencer

Thank you for your interest in contributing to Alexa Silencer! We welcome contributions from the community and appreciate your help in making this project better.

## 🚀 Quick Start for Contributors

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/alexa-silencer.git
   cd alexa-silencer
   ```
3. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/macOS
   source .venv/bin/activate
   ```
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Make your changes** and test them
6. **Submit a pull request**

## 🐛 Reporting Issues

When reporting issues, please include:

- **Operating System** (Windows/Linux version)
- **Python version** (`python --version`)
- **Error messages** (full stack trace if applicable)
- **Steps to reproduce** the issue
- **Expected vs actual behavior**

### Log Files
Include relevant log files from:
- **Windows**: `%APPDATA%\AlexaSilencer\alexa_silencer.log`
- **Linux**: `~/.alexa_silencer/alexa_silencer.log`

## 💡 Feature Requests

We welcome feature requests! Please:

1. **Check existing issues** to avoid duplicates
2. **Describe the problem** you're trying to solve
3. **Propose a solution** if you have one in mind
4. **Consider compatibility** with both Windows and Linux

## 🔧 Development Guidelines

### Code Style
- Follow **PEP 8** Python style guidelines
- Use **clear, descriptive variable names**
- Add **docstrings** to functions and classes
- Keep functions **focused and small**

### Testing
- Test on both **Windows and Linux** if possible
- Run the test suite: `python test.py`
- Test the setup process: `python setup.py`
- Verify auto-startup functionality works

### Cross-Platform Considerations
- Use `pathlib.Path` for file paths
- Use `platform.system()` for OS detection
- Test platform-specific code paths
- Consider different audio systems across platforms

## 📋 Pull Request Process

1. **Update documentation** if needed
2. **Test your changes** thoroughly
3. **Update CHANGELOG.md** if applicable
4. **Write clear commit messages**
5. **Reference related issues** in your PR description

### PR Requirements
- [ ] Code follows project style guidelines
- [ ] Changes have been tested on target platforms
- [ ] Documentation has been updated if needed
- [ ] No new linting errors or warnings
- [ ] Backwards compatibility is maintained

## 🏗️ Building Executables

To build standalone executables:

```bash
# Install build dependencies
pip install pyinstaller

# Build for current platform
python build.py
```

The executable will be created in the appropriate platform folder.

## 📁 Project Structure

```
alexa-silencer/
├── alexa_silencer.py          # Main application
├── requirements.txt           # Python dependencies
├── setup.py                  # Interactive setup script
├── setup.bat/.sh            # Platform setup helpers
├── build.py                  # Executable build script
├── test.py                   # Test suite
├── releases/                 # Pre-built executables (gitignored)
├── README.md                 # Project documentation
├── CONTRIBUTING.md           # This file
├── CHANGELOG.md              # Version history
├── LICENSE                   # MIT license
└── DEVELOPMENT.md            # Development notes
```

## 🤝 Code of Conduct

This project adheres to a simple code of conduct:

- **Be respectful** and professional
- **Be helpful** to other contributors
- **Focus on the code**, not personal attacks
- **Welcome newcomers** and help them learn

## 📞 Getting Help

- **Open an issue** for bugs or feature requests
- **Start a discussion** for general questions
- **Check existing documentation** first

## 🎯 Priority Areas for Contribution

We especially welcome contributions in these areas:

- **macOS support** (currently Windows/Linux only)
- **Additional audio backends** for better compatibility
- **Improved error handling** and recovery
- **Battery optimization** for laptops
- **GUI configuration tool** (optional)
- **Alternative scheduling methods** for different platforms

Thank you for contributing to Alexa Silencer! 🎉
