@echo off
python -m kgeb.cli --documents documents.txt --entities entities.json --entities-output entities_output.json --relations-output relations_output.json --evaluation-output evaluation_report.json
