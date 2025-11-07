#!/bin/sh
set -e
pytest -q
# Run baseline pipeline to generate outputs for manual review
python -m src.cli --docs documents.txt || true
