# Enterprise Knowledge Graph Extraction Benchmark (KGEB)

An open-source framework for evaluating AI methods on entity recognition and relation extraction from semi-structured enterprise text, providing a reproducible benchmark for enterprise knowledge graph construction.

## 🎯 Overview

KGEB is designed to evaluate and benchmark knowledge graph extraction methods on enterprise documents. It provides:

- **Entity Extraction**: Identify and extract 10 types of entities with their attributes
- **Relation Extraction**: Identify 30 types of relationships between entities
- **Evaluation Framework**: Comprehensive metrics including Precision, Recall, F1, Schema Compliance, and Logical Consistency
- **Reproducible Environment**: Docker, setup scripts, and automated testing

## 📋 Features

### Entity Types

The framework extracts the following entity types:

- **Person**: name, age, position, department
- **Company**: name, industry, sector, location
- **Project**: name, start_date, end_date, status, budget
- **Department**: name, head, employee_count
- **Position**: title, level, salary_range
- **Technology**: name, category, version
- **Location**: city, country, office_type
- **Team**: name, size, focus_area
- **Product**: name, version, release_date
- **Client**: name, contract_value, industry

### Relation Types

30 predefined relation types including:
- BelongsTo (Person → Department)
- WorksAt (Person → Company)
- ManagesProject (Person → Project)
- OwnsProject (Company → Project)
- UsesTechnology (Team → Technology)
- And 25 more relation types...

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or download the repository**

2. **Run the setup script**:
   ```bash
   bash setup.sh
   ```

   Or manually:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

### Running the Pipeline

**Option 1: One-click test script**
```bash
bash run_test.sh
```

**Option 2: Run the main pipeline**
```bash
python main.py
```

**Option 3: Run with custom options**
```bash
python main.py --documents documents.txt --output-dir ./output --method-name "My Method"
```

### Using Docker

```bash
# Build the Docker image
docker build -t kgeb .

# Run the container
docker run -v $(pwd)/output:/app/output kgeb
```

## 📁 Project Structure

```
.
├── documents.txt              # Input enterprise text documents
├── entities.json              # Entity type definitions
├── relations.json             # Relation type definitions
├── entity_extraction.py       # Entity extraction module
├── relation_extraction.py     # Relation extraction module
├── evaluator.py               # Evaluation framework
├── main.py                    # Main pipeline script
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker configuration
├── setup.sh                   # Setup script
├── run_test.sh                # One-click test script
├── tests/                     # Test suite
│   ├── test_entity_extraction.py
│   ├── test_relation_extraction.py
│   ├── test_evaluator.py
│   └── test_collaboration.py
├── test_report_template.md    # Test report template
└── README.md                  # This file
```

## 📊 Output Files

After running the pipeline, you'll get:

- **`entities_output.json`**: Extracted entities grouped by type
- **`relations_output.json`**: Extracted relations grouped by type
- **`evaluation_report.json`**: Comprehensive evaluation metrics

### Example Output

**entities_output.json**:
```json
{
  "Person": [
    {
      "name": "John Doe",
      "age": 32,
      "position": "Researcher",
      "department": "R&D"
    }
  ],
  "Company": [
    {
      "name": "OpenAI",
      "industry": "Technology",
      "sector": "Technology",
      "location": "San Francisco"
    }
  ]
}
```

**relations_output.json**:
```json
{
  "WorksAt": [
    {
      "person": "John Doe",
      "company": "OpenAI"
    }
  ],
  "ManagesProject": [
    {
      "person": "John Doe",
      "project": "Alpha"
    }
  ]
}
```

**evaluation_report.json**:
```json
{
  "method": "Baseline Method",
  "entity_f1": 0.85,
  "relation_f1": 0.78,
  "schema_compliance": "97.0%",
  "timestamp": "2025-11-07T12:30:00Z"
}
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_entity_extraction.py -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

### Test Coverage

The test suite includes:

- **Unit Tests**: Individual module testing
- **Integration Tests**: End-to-end pipeline testing
- **Collaboration Tests**: Multi-user, concurrent execution
- **Persistence Tests**: File I/O and data persistence
- **Multi-Document Tests**: Handling multiple documents

## 📈 Evaluation Metrics

The framework provides comprehensive evaluation:

### Entity Metrics

- **Precision**: Ratio of correctly extracted entities to all extracted entities
- **Recall**: Ratio of correctly extracted entities to all ground truth entities
- **F1 Score**: Harmonic mean of precision and recall
- **Schema Compliance**: Percentage of entities with all required attributes

### Relation Metrics

- **Precision**: Ratio of correctly extracted relations to all extracted relations
- **Recall**: Ratio of correctly extracted relations to all ground truth relations
- **F1 Score**: Harmonic mean of precision and recall
- **Schema Compliance**: Percentage of relations matching schema definition
- **Logical Consistency**: Percentage of relations referencing valid entities

## 🔧 Configuration

### Custom Entity Types

Edit `entities.json` to define custom entity types and attributes:

```json
{
  "CustomEntity": ["attribute1", "attribute2", "attribute3"]
}
```

### Custom Relation Types

Edit `relations.json` to define custom relation types:

```json
{
  "CustomRelation": {
    "description": "Description of the relation",
    "source_entity": "EntityType1",
    "target_entity": "EntityType2"
  }
}
```

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📝 License

[Specify your license here]

## 🙏 Acknowledgments

[Add acknowledgments if applicable]

## 📧 Contact

[Add contact information if applicable]

## 🔗 References

[Add references if applicable]

---

**Note**: This is a benchmark framework. For production use, consider integrating advanced NLP models (e.g., spaCy, Transformers) for improved extraction accuracy.

