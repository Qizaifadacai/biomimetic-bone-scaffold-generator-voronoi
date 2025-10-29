@echo off
REM Quick Start Script for Windows
REM Biomimetic Bone Scaffold Generator

title Biomimetic Bone Scaffold Generator - Quick Start

echo.
echo ========================================================
echo   Biomimetic Bone Scaffold Generator - Quick Start
echo ========================================================
echo.

REM Check Python installation
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.7 or higher.
    echo.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Found Python %PYTHON_VERSION%
echo.

REM Check dependencies
echo Checking dependencies...
python -c "import numpy, scipy, matplotlib" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing dependencies...
    echo.
    pip install -r requirements.txt
    
    if errorlevel 1 (
        echo.
        echo [ERROR] Installation failed. Please install manually:
        echo    pip install -r requirements.txt
        pause
        exit /b 1
    )
    
    echo.
    echo [OK] All dependencies installed successfully!
    echo.
) else (
    echo [OK] All dependencies are installed
    echo.
)

REM Run the demo
echo ========================================================
echo   Launching Interactive Demo...
echo ========================================================
echo.
echo Tips:
echo   * Enter numerical values in the text boxes
echo   * Press Enter to confirm
echo   * Click 'Generate Scaffold' to create
echo   * Click 'Save Visuals' to export images
echo.
echo Starting in 3 seconds...
timeout /t 3 /nobreak >nul

python 新版本演示.py

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to launch. Possible issues:
    echo   1. Missing main module
    echo   2. Display environment not available
    echo   3. Dependency errors
    echo.
    echo Try running manually:
    echo   python 新版本演示.py
    echo.
    pause
)
