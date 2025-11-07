@echo off
REM Quick Start Script for KGEB on Windows
REM Runs entity extraction, relation extraction, and evaluation in one command

setlocal enabledelayedexpansion

echo ================================
echo KGEB Quick Start - Windows
echo ================================
echo.

REM Setup
if not exist "venv" (
    echo Setting up virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate.bat
)

REM Run pipeline
echo Starting KGEB Pipeline...
echo.

python main.py ^
    --input documents.txt ^
    --output-dir output ^
    --data-dir . ^
    --method "KGEB-Baseline" ^
    --entities-schema entities.json ^
    --relations-schema relations.json

echo.
echo ================================
echo ✓ Quick start completed!
echo ================================
echo.
echo Output files:
echo   - Entities: output\entities\entities_output.json
echo   - Relations: output\relations\relations_output.json
echo   - Evaluation: output\evaluation\evaluation_report.json

endlocal
