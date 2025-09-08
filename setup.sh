#!/bin/bash

echo "Alexa Silencer Setup"
echo "===================="
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.6+ using your distribution's package manager"
    echo "Example: sudo apt install python3 python3-pip"
    echo
    read -p "Press Enter to exit..."
    exit 1
fi

# Check Python version
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "Found Python $python_version"

# Run the setup script
python3 setup.py

echo
read -p "Press Enter to exit..."
