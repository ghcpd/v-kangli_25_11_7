@echo off
REM Setup script for Enterprise Knowledge Graph Extraction Benchmark (KGEB) - Windows Version

echo ==========================================
echo KGEB Setup Script
echo ==========================================
echo.

REM Check Python version
echo Checking Python version...
python --version
if errorlevel 1 (
    echo Error: Python not found. Please install Python 3.8 or higher.
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo.
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        exit /b 1
    )
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    exit /b 1
)

REM Verify required files exist
echo.
echo Verifying required files...
if exist "documents.txt" (echo [OK] documents.txt) else (echo [WARN] documents.txt not found)
if exist "entities.json" (echo [OK] entities.json) else (echo [WARN] entities.json not found)
if exist "relations.json" (echo [OK] relations.json) else (echo [WARN] relations.json not found)

REM Create output directory
echo.
echo Creating output directory...
if not exist "output" mkdir output

echo.
echo ==========================================
echo Setup completed successfully!
echo ==========================================
echo.
echo To activate the virtual environment, run:
echo   venv\Scripts\activate.bat
echo.
echo To run the pipeline, execute:
echo   python main.py
echo.

