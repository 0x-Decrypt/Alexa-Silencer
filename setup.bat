@echo off
title Alexa Silencer Setup
echo.
echo Starting Alexa Silencer Setup...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.6+ from https://python.org
    echo.
    pause
    exit /b 1
)

REM Run the setup script
python setup.py

pause
