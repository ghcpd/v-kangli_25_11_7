# Enterprise Knowledge Graph Extraction Benchmark (KGEB)

This repository provides a reproducible baseline for entity and relation extraction from semi-structured enterprise text. It includes:

- Rule-based baseline extractor and relation recognizer
- Evaluation pipeline with precision/recall/F1 and schema compliance metrics
- Dockerfile and test scripts for reproducibility

## Quickstart
1. Create a virtualenv and install requirements:

   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt

2. Run the baseline pipeline (Windows):

   run_test.bat

3. View outputs:
   - `entities_output.json`
   - `relations_output.json`
   - `evaluation_report.json`

## Adding Methods
Implement new method scripts in `kgeb/` and provide a `gold_entities.json` for evaluation.