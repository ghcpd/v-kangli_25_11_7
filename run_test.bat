@echo off
REM Run the baseline extraction and evaluation
python -m kgeb.extractors
python -m kgeb.evaluator
if exist entities_output.json (echo Entities output written) else (echo Entities output not found)
if exist relations_output.json (echo Relations output written) else (echo Relations output not found)

echo Running tests...
pytest -q
