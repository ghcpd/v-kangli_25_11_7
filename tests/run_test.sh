#!/bin/bash

# KGEB Test Runner Script
# Runs comprehensive test suite and generates test reports

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
REPORT_DIR="$PROJECT_DIR/reports"

echo "================================"
echo "KGEB Test Suite Runner"
echo "================================"
echo ""

# Create reports directory
mkdir -p "$REPORT_DIR"

# Check if virtual environment exists
if [ ! -d "$PROJECT_DIR/venv" ]; then
    echo "Virtual environment not found. Creating..."
    cd "$PROJECT_DIR"
    python -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
else
    source "$PROJECT_DIR/venv/bin/activate"
fi

cd "$PROJECT_DIR"

echo "Running pytest with coverage..."
python -m pytest tests/test_kgeb.py -v --cov=. --cov-report=html:$REPORT_DIR/coverage --cov-report=json:$REPORT_DIR/coverage.json --tb=short -s

# Generate test report
echo ""
echo "================================"
echo "Test Execution Completed"
echo "================================"
echo ""
echo "Reports generated:"
echo "  - HTML Coverage Report: $REPORT_DIR/coverage/index.html"
echo "  - JSON Coverage Report: $REPORT_DIR/coverage.json"
echo ""

# Run specific test categories
echo "Running Reproducibility Tests..."
python -m pytest tests/test_kgeb.py::TestReproducibility -v

echo ""
echo "Running Persistence Tests..."
python -m pytest tests/test_kgeb.py::TestPersistence -v

echo ""
echo "Running Conflict Handling Tests..."
python -m pytest tests/test_kgeb.py::TestConflictHandling -v

echo ""
echo "Running Multi-Document Tests..."
python -m pytest tests/test_kgeb.py::TestMultiDocument -v

echo ""
echo "Running Schema Compliance Tests..."
python -m pytest tests/test_kgeb.py::TestSchemaCompliance -v

echo ""
echo "Running Integration Tests..."
python -m pytest tests/test_kgeb.py::TestIntegration -v

echo ""
echo "================================"
echo "✓ All tests completed!"
echo "================================"
