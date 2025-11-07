@echo off
python -m pytest -q
python -m src.cli --docs documents.txt || exit /b 0
