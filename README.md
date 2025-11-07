# Enterprise Knowledge Graph Extraction Benchmark (KGEB)

A reproducible framework for evaluating AI methods on entity recognition and relation extraction from semi-structured enterprise text, enabling enterprise knowledge graph construction.

## 🎯 Overview

KGEB provides a comprehensive benchmark for evaluating knowledge graph extraction systems with:

- **10 Entity Types**: Person, Company, Project, Department, Position, Technology, Location, Team, Product, Client
- **30 Relation Types**: Comprehensive relation definitions covering enterprise knowledge structures  
- **Unified Pipeline**: Complete workflow from extraction to evaluation with metrics
- **Reproducibility Framework**: Ensures consistent, repeatable results
- **Comprehensive Testing**: Tests for persistence, conflict handling, schema compliance, and multi-document behavior

## 📋 Functional Requirements

### 1. Entity Extraction Task

Extract and identify 10 entity types with their attributes:

```json
{
  "Person": ["name", "age", "position", "department"],
  "Company": ["name", "industry", "sector", "location"],
  "Project": ["name", "start_date", "end_date", "status", "budget"],
  "Department": ["name", "head", "employee_count"],
  "Position": ["title", "level", "salary_range"],
  "Technology": ["name", "category", "version"],
  "Location": ["city", "country", "office_type"],
  "Team": ["name", "size", "focus_area"],
  "Product": ["name", "version", "release_date"],
  "Client": ["name", "contract_value", "industry"]
}
```

**Output**: `entities_output.json` with extracted entities grouped by type

### 2. Relation Extraction Task

Extract relationships between entities (30+ relation types):
- BelongsTo, ManagesProject, WorksAt, HasPosition
- LocatedIn, OwnsProject, OperatesIn, HasDepartment
- UsesTechnology, ProducesProduct, HasTeam, PersonInTeam
- And 18+ additional relation types (see `relations.json`)

**Output**: `relations_output.json` with extracted relations grouped by type

### 3. Evaluation Framework

Comprehensive evaluation with metrics:
- **Precision, Recall, F1 Score** for entities and relations
- **Schema Compliance** validation
- **Logical Consistency** checking between entities and relations

**Output**: `evaluation_report.json` with detailed metrics and compliance results

## 🚀 Quick Start

### 1. Setup Environment

```bash
# On Linux/macOS
bash setup.sh

# On Windows
setup.bat
```

### 2. Run Pipeline

```bash
# On Linux/macOS
bash run_pipeline.sh

# On Windows
run_pipeline.bat
```

### 3. Run Tests

```bash
# On Linux/macOS
bash tests/run_test.sh

# On Windows
tests\run_test.bat
```

## 📁 Project Structure

```
KGEB/
├── documents.txt              # Input: Semi-structured enterprise text
├── entities.json              # Schema: Entity type definitions
├── relations.json             # Schema: Relation type definitions
├── entity_extractor.py        # Module: Entity extraction logic
├── relation_extractor.py      # Module: Relation extraction logic
├── evaluator.py              # Module: Evaluation framework
├── main.py                    # Pipeline: Main orchestrator
├── test_report_templates.py   # Templates: Test report generation
├── requirements.txt           # Dependencies: Python packages
├── setup.sh / setup.bat       # Setup: Environment initialization
├── run_pipeline.sh / .bat     # Automation: Quick pipeline execution
├── Dockerfile                 # Container: Docker configuration
├── .gitignore                 # Git: Ignore patterns
├── tests/
│   ├── test_kgeb.py          # Test suite: Comprehensive tests
│   ├── run_test.sh / .bat    # Test runner: Automated test execution
│   └── fixtures/             # Test fixtures and data
├── output/
│   ├── entities/             # Output: Extracted entities
│   ├── relations/            # Output: Extracted relations
│   └── evaluation/           # Output: Evaluation reports
└── reports/                  # Test reports and coverage
```

## 🔧 Usage

### Basic Pipeline Usage

```python
from main import KGEBPipeline

# Initialize pipeline
pipeline = KGEBPipeline(
    data_dir=".",
    output_dir="output",
    entities_schema="entities.json",
    relations_schema="relations.json"
)

# Run full pipeline
results = pipeline.run_full_pipeline(
    input_file="documents.txt",
    method_name="My-Method"
)
```

### Entity Extraction Only

```python
from entity_extractor import extract_entities

stats = extract_entities(
    input_file="documents.txt",
    output_file="output/entities/entities_output.json"
)
```

### Relation Extraction Only

```python
from relation_extractor import extract_relations

stats = extract_relations(
    text_file="documents.txt",
    entities_file="output/entities/entities_output.json",
    output_file="output/relations/relations_output.json"
)
```

### Evaluation Only

```python
from evaluator import EntityEvaluator, RelationEvaluator
import json

# Load results
with open("output/entities/entities_output.json") as f:
    predicted_entities = json.load(f)

# Calculate metrics
metrics = EntityEvaluator.calculate_metrics(
    gold_entities=predicted_entities,  # Gold standard
    predicted_entities=predicted_entities
)
```

## 🧪 Testing

The project includes comprehensive tests for:

1. **Reproducibility**: Same input produces identical output
2. **Persistence**: Results are properly saved and loaded
3. **Conflict Handling**: Duplicate entities are detected and handled correctly
4. **Multi-Document Behavior**: Multiple documents are processed consistently
5. **Schema Compliance**: Extracted data complies with schema
6. **Integration**: Full pipeline works end-to-end

### Run All Tests

```bash
# Linux/macOS
bash tests/run_test.sh

# Windows
tests\run_test.bat
```

### Run Specific Test Category

```bash
python -m pytest tests/test_kgeb.py::TestReproducibility -v
python -m pytest tests/test_kgeb.py::TestPersistence -v
python -m pytest tests/test_kgeb.py::TestConflictHandling -v
python -m pytest tests/test_kgeb.py::TestMultiDocument -v
python -m pytest tests/test_kgeb.py::TestSchemaCompliance -v
python -m pytest tests/test_kgeb.py::TestIntegration -v
```

## 📊 Output Examples

### entities_output.json

```json
{
  "Person": [
    {
      "name": "John Zhang",
      "age": 35,
      "position": "Engineer",
      "department": "R&D"
    }
  ],
  "Company": [
    {
      "name": "Tencent",
      "industry": "Technology",
      "sector": "Internet",
      "location": "Shenzhen"
    }
  ],
  "Project": [
    {
      "name": "Smart City Construction",
      "start_date": "2024-01-01",
      "end_date": "2025-12-31",
      "status": "Ongoing",
      "budget": 5000000
    }
  ]
}
```

### relations_output.json

```json
{
  "BelongsTo": [
    {"person": "John Zhang", "department": "R&D"}
  ],
  "OwnsProject": [
    {"company": "Tencent", "project": "Smart City Construction"}
  ],
  "UsesTechnology": [
    {"team": "AI R&D Team", "technology": "Deep Learning Platform"}
  ]
}
```

### evaluation_report.json

```json
{
  "method": "KGEB-Baseline",
  "timestamp": "2025-11-07T12:30:00Z",
  "entity_metrics": {
    "overall_precision": 0.85,
    "overall_recall": 0.82,
    "overall_f1": 0.8351,
    "by_type": {
      "Person": {"precision": 0.88, "recall": 0.85, "f1_score": 0.8649}
    }
  },
  "relation_metrics": {
    "overall_precision": 0.78,
    "overall_recall": 0.75,
    "overall_f1": 0.7641,
    "by_type": {}
  },
  "schema_compliance": {
    "entity_compliance": 0.97,
    "relation_compliance": 0.95
  }
}
```

## 🐳 Docker Support

Build and run using Docker:

```bash
# Build image
docker build -t kgeb:latest .

# Run container
docker run -v $(pwd)/data:/app/data -v $(pwd)/output:/app/output kgeb:latest

# Run with custom input
docker run -v $(pwd)/data:/app/data -v $(pwd)/output:/app/output kgeb:latest \
  python main.py --input data/documents.txt
```

## 📦 Dependencies

- Python 3.8+
- pydantic 2.5.0
- jsonschema 4.20.0
- pytest 7.4.3
- numpy 1.24.3
- pandas 2.1.1

See `requirements.txt` for complete list.

## 🤝 Contributing

To extend KGEB:

1. Add new entity types to `entities.json`
2. Add new relation types to `relations.json`
3. Implement extraction logic in respective modules
4. Add tests to ensure quality
5. Update documentation

## 📋 Evaluation Metrics

### Entity Extraction Metrics

- **Precision**: Correctly extracted entities / Total extracted entities
- **Recall**: Correctly extracted entities / Total gold entities
- **F1 Score**: Harmonic mean of precision and recall
- **Schema Compliance**: Percentage of entities complying with schema

### Relation Extraction Metrics

- **Precision**: Correctly extracted relations / Total extracted relations
- **Recall**: Correctly extracted relations / Total gold relations
- **F1 Score**: Harmonic mean of precision and recall
- **Logical Consistency**: Relations consistent with entity types

## 🔍 Advanced Usage

### Custom Configuration

```python
from main import KGEBPipeline

pipeline = KGEBPipeline(
    data_dir="data/",
    output_dir="results/",
    entities_schema="config/entities_custom.json",
    relations_schema="config/relations_custom.json"
)

results = pipeline.run_full_pipeline(
    input_file="documents.txt",
    method_name="Custom-Method-v1"
)
```

### Batch Processing

```python
from pathlib import Path
from main import KGEBPipeline

pipeline = KGEBPipeline()
results = []

for doc_file in Path("documents/").glob("*.txt"):
    result = pipeline.run_full_pipeline(str(doc_file))
    results.append(result)
```

## 📖 Citation

If you use KGEB in your research, please cite:

```
@software{kgeb2025,
  title={Enterprise Knowledge Graph Extraction Benchmark},
  author={KGEB Contributors},
  year={2025},
  url={https://github.com/ghcpd/v-kangli_25_11_7}
}
```

## 📝 License

This project is provided as-is for research and development purposes.

## 🆘 Support

For issues and questions:
1. Check existing documentation
2. Review test examples
3. Check test output and logs
4. Refer to docstrings in source code