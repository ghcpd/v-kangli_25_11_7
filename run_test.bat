@echo off
REM Run extractor, relations, and evaluation
python kgeb\extract.py --docs documents.txt --entities entities.json --out entities_output.json
python kgeb\relations.py --docs documents.txt --relations relations.json --out relations_output.json
REM You should provide or generate gold entities for evaluation: gold_entities.json
python kgeb\evaluate.py --gold gold_entities.json --pred entities_output.json --schema entities.json --out evaluation_report.json
pause
