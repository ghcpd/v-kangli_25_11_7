#!/bin/bash

# Quick Start Script for KGEB
# Runs entity extraction, relation extraction, and evaluation in one command

set -e

echo "================================"
echo "KGEB Quick Start"
echo "================================"
echo ""

# Setup
if [ ! -d "venv" ]; then
    echo "Setting up virtual environment..."
    python -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Run pipeline
echo "Starting KGEB Pipeline..."
echo ""

python main.py \
    --input documents.txt \
    --output-dir output \
    --data-dir . \
    --method "KGEB-Baseline" \
    --entities-schema entities.json \
    --relations-schema relations.json

echo ""
echo "================================"
echo "✓ Quick start completed!"
echo "================================"
echo ""
echo "Output files:"
echo "  - Entities: output/entities/entities_output.json"
echo "  - Relations: output/relations/relations_output.json"
echo "  - Evaluation: output/evaluation/evaluation_report.json"
