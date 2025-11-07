#!/usr/bin/env bash
# Run the extractor and evaluator against gold standard for the repository
python src/extractors.py documents.txt
python -m src.evaluator --pred_entities entities_output.json --gold_entities tests/data/gold_entities.json --pred_relations relations_output.json --gold_relations tests/data/gold_relations.json --schema entities.json
pytest -q
