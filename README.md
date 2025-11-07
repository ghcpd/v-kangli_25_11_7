# Enterprise Knowledge Graph Extraction Benchmark (KGEB)

This repository contains a baseline rule-based extraction and evaluation framework for enterprise entity and relation extraction.

## Project Overview

Enterprise Knowledge Graph Extraction Benchmark (KGEB) aims to provide an open, reproducible baseline for entity and relation extraction on semi-structured enterprise text.

### Contents
- `documents.txt` — the semi-structured text corpus used for baseline testing.
- `entities.json` — entity definitions and schema fields.
- `relations.json` — relation types and participating entity types.
- `kgeb/` — Python package with baseline extractors, evaluation code and utilities.
- `entities_output.json` — output produced by baseline extractor (created when running the extractor).
- `relations_output.json` — relations output produced by baseline extractor.
- `evaluation_report.json` — evaluation metrics produced by the evaluation pipeline.
- `tests/` — pytest tests verifying pipeline operations and conflict handling.

### How to run
1. Install dependencies: `setup.bat` or `./setup.sh`.
2. Generate gold labels (optional): `python -m kgeb.gold_generator`.
3. Run baseline extractor & evaluator: `run_test.bat` (Windows) or `./run_test.sh` (Linux/macOS).

### Extending & Reproducing
- Add improved extractors under `kgeb/extractors.py` or create new modules.
- Add new relation types to `relations.json`.
- Provide `entities_gold.json` and `relations_gold.json` to evaluate against ground truth.

Usage:
- Run setup: `setup.bat` (Windows) or `./setup.sh` (Linux/macOS)
- Run the baseline extraction and evaluation: `run_test.bat` (Windows) or `./run_test.sh` (Linux/macOS)

Outputs will be written to `entities_output.json`, `relations_output.json`, and `evaluation_report.json`.
