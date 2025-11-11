#!/bin/bash
# One-click test script for Enterprise Knowledge Graph Extraction Benchmark (KGEB)

set -e

echo "=========================================="
echo "KGEB Test Runner"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment not found. Running setup...${NC}"
    bash setup.sh
fi

# Activate virtual environment
source venv/bin/activate

# Run main pipeline
echo ""
echo "Running KGEB pipeline..."
echo ""

if python main.py; then
    echo ""
    echo -e "${GREEN}✓ Pipeline execution successful${NC}"
else
    echo ""
    echo -e "${RED}✗ Pipeline execution failed${NC}"
    exit 1
fi

# Run automated tests if pytest is available
if command -v pytest &> /dev/null; then
    echo ""
    echo "Running automated tests..."
    echo ""
    
    if pytest tests/ -v --tb=short; then
        echo ""
        echo -e "${GREEN}✓ All tests passed${NC}"
    else
        echo ""
        echo -e "${RED}✗ Some tests failed${NC}"
        exit 1
    fi
else
    echo ""
    echo -e "${YELLOW}Warning: pytest not found. Skipping automated tests.${NC}"
    echo "Install pytest to run tests: pip install pytest"
fi

# Display results summary
echo ""
echo "=========================================="
echo "Test Results Summary"
echo "=========================================="
echo ""

if [ -f "evaluation_report.json" ]; then
    echo "Evaluation Report:"
    python -c "
import json
with open('evaluation_report.json', 'r') as f:
    report = json.load(f)
    print(f\"  Method: {report.get('method', 'N/A')}\")
    print(f\"  Entity F1: {report.get('entity_f1', 0):.3f}\")
    print(f\"  Relation F1: {report.get('relation_f1', 0):.3f}\")
    print(f\"  Schema Compliance: {report.get('schema_compliance', 'N/A')}\")
"
else
    echo -e "${YELLOW}Warning: evaluation_report.json not found${NC}"
fi

echo ""
echo "Output files:"
[ -f "entities_output.json" ] && echo -e "  ${GREEN}✓${NC} entities_output.json" || echo -e "  ${RED}✗${NC} entities_output.json"
[ -f "relations_output.json" ] && echo -e "  ${GREEN}✓${NC} relations_output.json" || echo -e "  ${RED}✗${NC} relations_output.json"
[ -f "evaluation_report.json" ] && echo -e "  ${GREEN}✓${NC} evaluation_report.json" || echo -e "  ${RED}✗${NC} evaluation_report.json"

echo ""
echo "=========================================="
echo "Test execution completed!"
echo "=========================================="

