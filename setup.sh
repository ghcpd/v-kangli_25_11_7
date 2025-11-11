#!/bin/bash
# Setup script for Enterprise Knowledge Graph Extraction Benchmark (KGEB)

set -e

echo "=========================================="
echo "KGEB Setup Script"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

# Check if Python 3.8+
if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    echo "Error: Python 3.8 or higher is required"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Verify required files exist
echo ""
echo "Verifying required files..."
required_files=("documents.txt" "entities.json" "relations.json")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "Warning: $file not found"
    else
        echo "✓ $file found"
    fi
done

# Create output directory
echo ""
echo "Creating output directory..."
mkdir -p output

# Make scripts executable
echo ""
echo "Making scripts executable..."
chmod +x run_test.sh 2>/dev/null || true

echo ""
echo "=========================================="
echo "Setup completed successfully!"
echo "=========================================="
echo ""
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "To run the pipeline, execute:"
echo "  python main.py"
echo ""

