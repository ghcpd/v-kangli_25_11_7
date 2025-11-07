@echo off
REM Usage: run_test_verbose.bat (python_path)
if "%1"=="" (
  set PY=python
) else (
  set PY=%1
)
cd /d %~dp0\..\
%PY% -m pytest -q > test_results.txt 2>&1 || true
type test_results.txt
echo WROTE test_results.txt in %CD%
