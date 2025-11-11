@echo off
REM One-click test script for Enterprise Knowledge Graph Extraction Benchmark (KGEB) - Windows Version

echo ==========================================
echo KGEB Test Runner
echo ==========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Virtual environment not found. Running setup...
    call setup.bat
    if errorlevel 1 (
        echo Setup failed. Please run setup.bat manually.
        exit /b 1
    )
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run main pipeline
echo.
echo Running KGEB pipeline...
echo.

python main.py
if errorlevel 1 (
    echo.
    echo Pipeline execution failed
    exit /b 1
) else (
    echo.
    echo Pipeline execution successful
)

REM Run automated tests if pytest is available
where pytest >nul 2>&1
if %errorlevel% equ 0 (
    echo.
    echo Running automated tests...
    echo.
    
    pytest tests\ -v --tb=short
    if errorlevel 1 (
        echo.
        echo Some tests failed
        exit /b 1
    ) else (
        echo.
        echo All tests passed
    )
) else (
    echo.
    echo Warning: pytest not found. Skipping automated tests.
    echo Install pytest to run tests: pip install pytest
)

REM Display results summary
echo.
echo ==========================================
echo Test Results Summary
echo ==========================================
echo.

if exist "evaluation_report.json" (
    echo Evaluation Report:
    python -c "import json; f=open('evaluation_report.json','r'); r=json.load(f); print('  Method: ' + r.get('method','N/A')); print('  Entity F1: {:.3f}'.format(r.get('entity_f1',0))); print('  Relation F1: {:.3f}'.format(r.get('relation_f1',0))); print('  Schema Compliance: ' + r.get('schema_compliance','N/A'))"
) else (
    echo Warning: evaluation_report.json not found
)

echo.
echo Output files:
if exist "entities_output.json" (echo   [OK] entities_output.json) else (echo   [FAIL] entities_output.json)
if exist "relations_output.json" (echo   [OK] relations_output.json) else (echo   [FAIL] relations_output.json)
if exist "evaluation_report.json" (echo   [OK] evaluation_report.json) else (echo   [FAIL] evaluation_report.json)

echo.
echo ==========================================
echo Test execution completed!
echo ==========================================

