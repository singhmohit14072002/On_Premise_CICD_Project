@echo off
title DevOps Animation Launcher
echo.
echo ========================================
echo    DevOps Animation Launcher
echo ========================================
echo.
echo Starting DevOps Animation Dashboard...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.6 or higher from https://python.org
    echo.
    pause
    exit /b 1
)

REM Run the launcher
python run_devops_animation.py

REM If there was an error, pause to show the message
if errorlevel 1 (
    echo.
    echo An error occurred while running the application.
    pause
) 