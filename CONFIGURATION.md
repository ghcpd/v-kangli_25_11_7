# KGEB Configuration Guide

This document provides detailed configuration options for the KGEB system.

## Entity Schema Configuration

The `entities.json` file defines the entity types and their attributes.

### Adding New Entity Types

```json
{
  "Person": ["name", "age", "position", "department"],
  "Company": ["name", "industry", "sector", "location"],
  "NewEntityType": ["attr1", "attr2", "attr3"]
}
```

### Modifying Existing Entity Types

1. Edit `entities.json`
2. Update corresponding extraction patterns in `entity_extractor.py`
3. Add tests for the new attributes
4. Update evaluation schema

## Relation Schema Configuration

The `relations.json` file defines the relation types and their participating entities.

### Relation Schema Structure

```json
{
  "relations": [
    {
      "id": "RelationType",
      "name": "Human-readable name",
      "source_entity": "SourceType",
      "target_entity": "TargetType",
      "description": "Relation description"
    }
  ]
}
```

### Adding New Relation Types

1. Add entry to `relations.json`
2. Implement extraction logic in `relation_extractor.py`
3. Add test cases
4. Update evaluation framework

## Pipeline Configuration

### Command-line Options

```bash
python main.py --help
```

Options:
- `--input`: Input document file (default: documents.txt)
- `--output-dir`: Output directory (default: output)
- `--data-dir`: Data directory (default: .)
- `--method`: Method name (default: KGEB-Baseline)
- `--entities-schema`: Entities schema path (default: entities.json)
- `--relations-schema`: Relations schema path (default: relations.json)

### Programmatic Configuration

```python
from main import KGEBPipeline

pipeline = KGEBPipeline(
    data_dir="path/to/data",
    output_dir="path/to/output",
    entities_schema="custom_entities.json",
    relations_schema="custom_relations.json"
)
```

## Environment Variables

Create a `.env` file in the project root:

```
KGEB_ENV=development  # or production
KGEB_LOG_LEVEL=DEBUG
KGEB_DATA_DIR=./data
KGEB_OUTPUT_DIR=./output
```

## Docker Configuration

### Dockerfile Parameters

Edit `Dockerfile` to customize:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install custom dependencies
RUN apt-get update && apt-get install -y \
    custom-package-1 \
    custom-package-2
```

### Docker Compose (Optional)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  kgeb:
    build: .
    volumes:
      - ./data:/app/data
      - ./output:/app/output
    environment:
      - KGEB_ENV=production
      - KGEB_LOG_LEVEL=INFO
    command: python main.py --input data/documents.txt
```

## Extraction Pattern Customization

### Entity Extraction Patterns

In `entity_extractor.py`, modify regex patterns:

```python
# Pattern for Person entity
person_pattern = r"(\w+\s+\w+),\s*age\s+(\d+),\s*works at\s+(.+?)\s+as\s+(.+?)(?:\.|,)"
```

### Relation Extraction Patterns

In `relation_extractor.py`, modify relation patterns:

```python
# Pattern for WorksAt relation
person_company_pattern = r"(\w+\s+\w+),\s*age\s+\d+,\s*works at\s+(.+?)\s+as\s+"
```

## Evaluation Configuration

### Schema Validation Rules

Customize validation in `evaluator.py`:

```python
class SchemaValidator:
    def validate_entities(self, entities):
        # Custom validation logic
        pass
```

### Metrics Calculation

Adjust metric thresholds:

```python
COMPLIANCE_THRESHOLD = 0.95  # 95% compliance required
F1_THRESHOLD = 0.70          # 70% F1 score threshold
```

## Testing Configuration

### Pytest Configuration

Create `pytest.ini`:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short --strict-markers
```

### Test Markers

Add custom markers for test categorization:

```python
# In conftest.py
def pytest_configure(config):
    config.addinivalue_line("markers", "slow: marks tests as slow")
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
```

## Performance Tuning

### Memory Management

For large documents, adjust batch size:

```python
BATCH_SIZE = 1000  # Process documents in batches
```

### Parallel Processing (Optional)

Configure multiprocessing:

```python
from multiprocessing import Pool

NUM_WORKERS = 4  # Number of parallel workers
```

## Logging Configuration

Create `logging.ini`:

```ini
[loggers]
keys=root,kgeb

[handlers]
keys=console,file

[formatters]
keys=standard

[logger_root]
level=DEBUG
handlers=console

[logger_kgeb]
level=DEBUG
handlers=file
qualname=kgeb

[handler_console]
class=StreamHandler
level=DEBUG
formatter=standard
args=(sys.stdout,)

[handler_file]
class=FileHandler
level=DEBUG
formatter=standard
args=('logs/kgeb.log',)

[formatter_standard]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
datefmt=%Y-%m-%d %H:%M:%S
```

## Integration with External Systems

### API Integration

Extend `main.py` to integrate with external APIs:

```python
import requests

def get_external_entities(source_url):
    response = requests.get(source_url)
    return response.json()
```

### Database Integration

Store results in database:

```python
from sqlalchemy import create_engine

engine = create_engine('postgresql://user:password@localhost/kgeb')
```

## Customization Examples

### Example 1: Custom Entity Type

Add a custom entity type `Organization`:

1. Update `entities.json`:
```json
{
  "Organization": ["name", "type", "sector", "headquarters"]
}
```

2. Add extraction pattern in `entity_extractor.py`:
```python
org_pattern = r"Organization:\s+(.+?),\s+type:\s+(.+?),"
```

3. Add test case in `tests/test_kgeb.py`

### Example 2: Custom Relation Type

Add custom relation `CompetsWith`:

1. Update `relations.json`:
```json
{
  "relations": [
    {
      "id": "CompetsWith",
      "name": "Company competes with Company",
      "source_entity": "Company",
      "target_entity": "Company"
    }
  ]
}
```

2. Implement in `relation_extractor.py`
3. Add test case

## Best Practices

1. **Always validate schemas** before deployment
2. **Test custom patterns** thoroughly
3. **Document configuration changes** in version control
4. **Monitor extraction quality** with test suite
5. **Keep patterns simple and maintainable**
6. **Use meaningful entity/relation type names**
7. **Provide examples in schema documentation**
8. **Review evaluation metrics regularly**
9. **Maintain test coverage above 90%**
10. **Use type hints in custom code**

## Troubleshooting Configuration Issues

### Issue: Entity extraction not finding entities

**Solution**: Check regex pattern in `entity_extractor.py`

### Issue: Relations not extracted correctly

**Solution**: Verify entity lookup in relation extractor works

### Issue: Schema validation failing

**Solution**: Ensure all required attributes are present

### Issue: Low F1 scores

**Solution**: Review extraction patterns and adjust thresholds

## Version Compatibility

- Python: 3.8+
- pydantic: 2.5.0+
- jsonschema: 4.20.0+
- pytest: 7.4.3+

## Additional Resources

- See `README.md` for quick start guide
- Check `entity_extractor.py` for entity extraction details
- Review `relation_extractor.py` for relation extraction logic
- See `evaluator.py` for evaluation framework documentation
- Check test files for usage examples
