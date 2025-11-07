@echo off
REM KGEB Test Runner Script for Windows
REM Runs comprehensive test suite and generates test reports

setlocal enabledelayedexpansion

set SCRIPT_DIR=%~dp0
set PROJECT_DIR=%SCRIPT_DIR%..
set REPORT_DIR=%PROJECT_DIR%\reports

echo ================================
echo KGEB Test Suite Runner - Windows
echo ================================
echo.

REM Create reports directory
if not exist "%REPORT_DIR%" mkdir "%REPORT_DIR%"

REM Check if virtual environment exists
if not exist "%PROJECT_DIR%\venv" (
    echo Virtual environment not found. Creating...
    cd /d "%PROJECT_DIR%"
    python -m venv venv
    call venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    pip install -r requirements.txt
) else (
    call "%PROJECT_DIR%\venv\Scripts\activate.bat"
)

cd /d "%PROJECT_DIR%"

echo Running pytest with coverage...
python -m pytest tests\test_kgeb.py -v --cov=. --cov-report=html:%REPORT_DIR%\coverage --cov-report=json:%REPORT_DIR%\coverage.json --tb=short -s

echo.
echo ================================
echo Test Execution Completed
echo ================================
echo.
echo Reports generated:
echo   - HTML Coverage Report: %REPORT_DIR%\coverage\index.html
echo   - JSON Coverage Report: %REPORT_DIR%\coverage.json
echo.

echo Running Reproducibility Tests...
python -m pytest tests\test_kgeb.py::TestReproducibility -v

echo.
echo Running Persistence Tests...
python -m pytest tests\test_kgeb.py::TestPersistence -v

echo.
echo Running Conflict Handling Tests...
python -m pytest tests\test_kgeb.py::TestConflictHandling -v

echo.
echo Running Multi-Document Tests...
python -m pytest tests\test_kgeb.py::TestMultiDocument -v

echo.
echo Running Schema Compliance Tests...
python -m pytest tests\test_kgeb.py::TestSchemaCompliance -v

echo.
echo Running Integration Tests...
python -m pytest tests\test_kgeb.py::TestIntegration -v

echo.
echo ================================
echo ✓ All tests completed!
echo ================================

endlocal
