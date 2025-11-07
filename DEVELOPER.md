# KGEB Developer Guide

This document provides guidance for extending and maintaining KGEB.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Input Documents                       │
└────────────────────┬────────────────────────────────────┘
                     │
         ┌───────────▼───────────┐
         │ Entity Extraction     │
         │ (entity_extractor.py) │
         └───────────┬───────────┘
                     │
         ┌───────────▼──────────────┐
         │ Relation Extraction      │
         │ (relation_extractor.py)  │
         └───────────┬──────────────┘
                     │
         ┌───────────▼──────────┐
         │ Evaluation Framework │
         │ (evaluator.py)       │
         └───────────┬──────────┘
                     │
         ┌───────────▼──────────────┐
         │ Report Generation         │
         │ (evaluation_report.json)  │
         └──────────────────────────┘
```

## Module Descriptions

### entity_extractor.py

Handles entity extraction from text.

**Key Classes:**
- `EntityExtractor`: Main class for entity extraction
- `ExtractedEntity`: Data class representing extracted entities

**Key Methods:**
- `extract_from_text(text)`: Extract entities from text
- `extract_from_file(filepath)`: Extract entities from file
- `save_results(filepath)`: Save results to JSON

**Extension Points:**
- Add new entity types in `ENTITY_SCHEMA`
- Implement extraction patterns for new types
- Customize `_process_line()` for new patterns

### relation_extractor.py

Handles relation extraction between entities.

**Key Classes:**
- `RelationExtractor`: Main class for relation extraction
- `Relation`: Data class representing extracted relations

**Key Methods:**
- `extract_from_text(text, entities)`: Extract relations from text
- `extract_from_file(text_file, entities_file)`: Extract from files
- `save_results(filepath)`: Save results to JSON

**Extension Points:**
- Add new relation types in `relations.json`
- Implement extraction patterns in `_extract_relations_from_line()`
- Customize entity matching logic

### evaluator.py

Handles evaluation and metrics calculation.

**Key Classes:**
- `SchemaValidator`: Validates schema compliance
- `EntityEvaluator`: Calculates entity metrics
- `RelationEvaluator`: Calculates relation metrics
- `EvaluationReport`: Generates reports

**Key Methods:**
- `validate_entities(entities)`: Validate entity schema
- `calculate_metrics(gold, predicted)`: Calculate precision/recall/F1
- `generate_report()`: Generate comprehensive report

**Extension Points:**
- Customize validation rules
- Add new evaluation metrics
- Implement custom scoring functions

### main.py

Orchestrates the complete pipeline.

**Key Classes:**
- `KGEBPipeline`: Main pipeline orchestrator

**Key Methods:**
- `extract_entities()`: Run entity extraction
- `extract_relations()`: Run relation extraction
- `evaluate()`: Run evaluation
- `run_full_pipeline()`: Run complete pipeline

## Adding a New Entity Type

### Step 1: Update Schema

Edit `entities.json`:

```json
{
  "NewEntity": ["attr1", "attr2", "attr3"]
}
```

### Step 2: Implement Extraction

Add to `entity_extractor.py`:

```python
def _extract_new_entity(self, line: str) -> None:
    pattern = r"NewEntity:\s+(.+?),\s+attr1:\s+(.+?),\s+"
    matches = re.finditer(pattern, line, re.IGNORECASE)
    for match in matches:
        value1, value2 = match.groups()
        entity_key = f"NewEntity_{value1}"
        if entity_key not in self.seen_entities:
            self.seen_entities.add(entity_key)
            self.extracted_entities["NewEntity"].append({
                "attr1": value1.strip(),
                "attr2": value2.strip(),
                "attr3": None
            })

# Call in _process_line()
self._extract_new_entity(line)
```

### Step 3: Write Tests

Add to `tests/test_kgeb.py`:

```python
def test_new_entity_extraction(self):
    test_text = "NewEntity: Value1, attr1: Data1, attr2: Data2"
    extractor = EntityExtractor()
    result = extractor.extract_from_text(test_text)
    assert len(result['NewEntity']) == 1
    assert result['NewEntity'][0]['attr1'] == 'Value1'
```

## Adding a New Relation Type

### Step 1: Update Relations Schema

Edit `relations.json`:

```json
{
  "relations": [
    {
      "id": "NewRelationType",
      "name": "Entity1 relates to Entity2",
      "source_entity": "Entity1",
      "target_entity": "Entity2",
      "description": "Description"
    }
  ]
}
```

### Step 2: Implement Extraction

Add to `relation_extractor.py`:

```python
def _extract_new_relation(self, line: str, entities: Dict) -> None:
    pattern = r"(\w+)\s+relates to\s+(\w+)"
    matches = re.finditer(pattern, line, re.IGNORECASE)
    for match in matches:
        entity1, entity2 = match.groups()
        rel_key = (entity1, entity2, "NewRelationType")
        if rel_key not in self.seen_relations:
            self.seen_relations.add(rel_key)
            self.extracted_relations["NewRelationType"].append({
                "entity1": entity1,
                "entity2": entity2
            })

# Call in _extract_relations_from_line()
self._extract_new_relation(line, all_entities)
```

### Step 3: Write Tests

Add to `tests/test_kgeb.py`:

```python
def test_new_relation_extraction(self):
    test_text = "Entity1 relates to Entity2"
    entities = {"Entity1": [], "Entity2": []}
    extractor = RelationExtractor()
    result = extractor.extract_from_text(test_text, entities)
    assert len(result['NewRelationType']) == 1
```

## Adding Custom Evaluation Metrics

### Step 1: Extend Evaluator

Add to `evaluator.py`:

```python
class CustomEvaluator:
    @staticmethod
    def calculate_custom_metric(gold, predicted):
        # Custom metric logic
        return custom_score
```

### Step 2: Integrate into Pipeline

Modify `main.py`:

```python
from evaluator import CustomEvaluator

custom_metric = CustomEvaluator.calculate_custom_metric(gold, predicted)
report['custom_metric'] = custom_metric
```

## Testing Guidelines

### Test Structure

```python
class TestCategory:
    def test_specific_behavior(self):
        # Arrange
        test_data = setup_test_data()
        
        # Act
        result = perform_action(test_data)
        
        # Assert
        assert result == expected_result
```

### Running Tests

```bash
# All tests
python -m pytest tests/ -v

# Specific test
python -m pytest tests/test_kgeb.py::TestClass::test_method -v

# With coverage
python -m pytest tests/ --cov=. --cov-report=html
```

## Code Style

Follow these conventions:

1. **Type Hints**: Use type hints for all function parameters and returns
```python
def extract_entities(text: str) -> Dict[str, List[Dict[str, Any]]]:
    pass
```

2. **Docstrings**: Provide docstrings for all classes and methods
```python
def extract_entities(self, text: str) -> Dict[str, Any]:
    """Extract entities from text.
    
    Args:
        text: Raw text document
        
    Returns:
        Dictionary of extracted entities grouped by type
    """
```

3. **Naming**: Use descriptive names
```python
person_names = {}  # Good
pn = {}            # Bad
```

4. **Line Length**: Keep lines under 100 characters

5. **Imports**: Organize imports (standard library, third-party, local)
```python
import json
import re
from typing import Dict

import pytest

from entity_extractor import EntityExtractor
```

## Performance Optimization

### For Large Documents

```python
# Process in chunks
CHUNK_SIZE = 10000  # characters

for chunk in text_chunks(document, CHUNK_SIZE):
    entities.extend(extractor.extract_from_text(chunk))
```

### For Relation Extraction

```python
# Pre-index entities for faster lookup
entity_index = {}
for etype, entities in all_entities.items():
    for entity in entities:
        entity_index[entity['name']] = (etype, entity)
```

## Debugging

### Enable Detailed Logging

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug(f"Processing: {line}")
logger.info(f"Extracted {count} entities")
logger.warning(f"Unusual pattern found: {pattern}")
logger.error(f"Failed to extract: {text}")
```

### Use Debugging Tools

```python
# Print intermediate results
import pprint
pprint.pprint(result)

# Use debugger
import pdb; pdb.set_trace()
```

## Release Checklist

- [ ] All tests pass (100% success rate)
- [ ] Code coverage above 90%
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version number updated
- [ ] No breaking changes documented
- [ ] Performance tests pass
- [ ] Docker image builds successfully
- [ ] README examples work

## Contributing Workflow

1. Fork repository
2. Create feature branch: `git checkout -b feature/new-entity-type`
3. Make changes and add tests
4. Run test suite: `bash tests/run_test.sh`
5. Commit changes: `git commit -m "Add new entity type"`
6. Push to branch: `git push origin feature/new-entity-type`
7. Create Pull Request

## Documentation

### Adding Documentation

1. Update docstrings in code
2. Update relevant README section
3. Add examples in documentation
4. Update CONFIGURATION.md if applicable
5. Add test cases as examples

### Documentation Format

Use Markdown with clear structure:

```markdown
## Feature Name

Brief description.

### Usage

Code example

### Configuration

Configuration details

### Troubleshooting

Common issues and solutions
```

## Version Management

Follow semantic versioning (MAJOR.MINOR.PATCH):

- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

Update in:
- `main.py`: `__version__`
- `setup.py`: `version`
- Documentation

## Additional Resources

- Python: https://docs.python.org/3/
- pytest: https://pytest.readthedocs.io/
- JSON Schema: https://json-schema.org/
- Regular Expressions: https://regex101.com/
- Type Hints: https://www.python.org/dev/peps/pep-0484/
