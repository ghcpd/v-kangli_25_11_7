#!/bin/sh
python -m src.cli --docs documents.txt --out-entities examples/entities_output.json --out-relations examples/relations_output.json || true
