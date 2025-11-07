# v-kangli_25_11_7

Enterprise Knowledge Graph Extraction Benchmark (KGEB)

This repository provides a reproducible framework to benchmark entity recognition and relation extraction from semi-structured enterprise text.

## Quick usage

- Install requirements: `pip install -r requirements.txt`
- Run the baseline extraction end-to-end: `python -m src.cli`
  - Output: `entities_output.json`, `relations_output.json`
- Run tests: `scripts/run_test.sh` (or `pytest -q`)

## Features

- Rule-based baseline entity & relation extraction
- Evaluation metrics: precision/recall/F1, schema compliance, relation consistency
- Reproducible runtime: `Dockerfile`, `setup.sh`, `requirements.txt`
- Automated tests using `pytest`

## Evaluation

- To evaluate over a gold standard, provide `--gold-entities` and `--gold-relations` to `src.cli`:
  - `python -m src.cli --gold-entities gold_entities.json --gold-relations gold_relations.json --out-eval evaluation_report.json`
- Generated evaluation report uses precision/recall/F1 for entities and relation consistency check.

## Notes

- This baseline uses simple heuristics and regex: it is intended to be a reproducible starting point. You can extend `src/extractor.py` and `src/relations.py` with model-based extractors.
- Tests check loader, extraction heuristics, relation inference, and multi-document deduplication.