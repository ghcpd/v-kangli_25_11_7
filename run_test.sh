#!/bin/bash
# Run the baseline extraction and evaluation
python -m kgeb.extractors
python -m kgeb.evaluator
if [ -f entities_output.json ]; then
  echo "Entities output written"
else
  echo "Entities output not found"
fi
if [ -f relations_output.json ]; then
  echo "Relations output written"
else
  echo "Relations output not found"
fi

echo "Running tests..."
pytest -q
