#!/bin/bash

# Enterprise Knowledge Graph Extraction Benchmark (KGEB) Setup Script
# This script sets up the development environment for KGEB

set -e

echo "================================"
echo "KGEB Project Setup"
echo "================================"

# Check Python version
echo "Checking Python version..."
python --version

# Create virtual environment
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python -m venv venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
echo "Creating project directories..."
mkdir -p data/raw
mkdir -p data/processed
mkdir -p output/entities
mkdir -p output/relations
mkdir -p output/evaluation
mkdir -p logs
mkdir -p tests/fixtures

# Download/prepare datasets (placeholder)
echo "Preparing data directories..."
if [ ! -f "data/raw/documents.txt" ]; then
    cp documents.txt data/raw/
fi
if [ ! -f "data/raw/entities.json" ]; then
    cp entities.json data/raw/
fi

echo "================================"
echo "✓ Setup completed successfully!"
echo "================================"
echo ""
echo "Next steps:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Run tests: python -m pytest tests/ -v"
echo "3. Run the pipeline: python main.py"
echo ""
