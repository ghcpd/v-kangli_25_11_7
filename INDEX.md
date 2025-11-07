# KGEB Complete Index & Quick Reference

## 📚 Documentation Map

### For Users

1. **START HERE**: `README.md`
   - Project overview
   - Quick start (5-10 minutes)
   - Basic usage examples
   - Output format reference

2. **Setup & Installation**: `README.md` → Quick Start section
   - Environment setup
   - Installation steps
   - Verification

3. **Configuration**: `CONFIGURATION.md`
   - All configuration options
   - Custom entity/relation types
   - Advanced settings
   - Troubleshooting

4. **Running Pipeline**: 
   - Quick: `bash run_pipeline.sh` (Unix) or `run_pipeline.bat` (Windows)
   - Manual: `python main.py [options]`
   - See `README.md` for options

5. **Testing**:
   - Run tests: `bash tests/run_test.sh` (Unix) or `tests\run_test.bat` (Windows)
   - See `README.md` → Testing section

### For Developers

1. **Architecture**: `DEVELOPER.md` → Architecture Overview
   - System design
   - Module structure
   - Data flow

2. **Adding Features**: `DEVELOPER.md`
   - Adding entity types (step-by-step)
   - Adding relation types (step-by-step)
   - Custom evaluation metrics
   - Code style guidelines

3. **Testing Guide**: `DEVELOPER.md` → Testing Guidelines
   - Writing tests
   - Running specific tests
   - Coverage targets

4. **API Reference**: Source code docstrings
   - `entity_extractor.py`: Entity extraction API
   - `relation_extractor.py`: Relation extraction API
   - `evaluator.py`: Evaluation API
   - `main.py`: Pipeline API

## 🗂️ File Organization

### Core Modules

| File | Purpose | Size | Status |
|------|---------|------|--------|
| `entity_extractor.py` | Entity extraction logic | ~500 lines | ✓ Complete |
| `relation_extractor.py` | Relation extraction logic | ~450 lines | ✓ Complete |
| `evaluator.py` | Evaluation framework | ~550 lines | ✓ Complete |
| `main.py` | Pipeline orchestration | ~350 lines | ✓ Complete |
| `test_report_templates.py` | Report generation | ~400 lines | ✓ Complete |

### Configuration Files

| File | Purpose | Content |
|------|---------|---------|
| `entities.json` | Entity schema | 10 entity types + attributes |
| `relations.json` | Relation schema | 30+ relation type definitions |
| `requirements.txt` | Python dependencies | 8 packages with versions |
| `Dockerfile` | Docker setup | Python 3.11-slim + dependencies |
| `.gitignore` | Git configuration | Python and IDE patterns |

### Documentation

| File | Audience | Length | Topics |
|------|----------|--------|--------|
| `README.md` | Everyone | ~400 lines | Overview, quick start, usage, examples |
| `CONFIGURATION.md` | Developers | ~350 lines | Config options, customization, troubleshooting |
| `DEVELOPER.md` | Developers | ~400 lines | Architecture, extension, testing, contributing |
| `PROJECT_SUMMARY.md` | Project Managers | ~300 lines | Status, deliverables, completion checklist |
| `THIS FILE` | Everyone | Reference | Quick lookup and navigation |

### Testing

| File | Purpose | Test Count |
|------|---------|-----------|
| `tests/test_kgeb.py` | Main test suite | 12 test cases covering 6 categories |
| `tests/run_test.sh` | Unix test runner | Auto-setup + coverage + categorized runs |
| `tests/run_test.bat` | Windows test runner | Auto-setup + coverage + categorized runs |

### Scripts

| Script | Platform | Purpose |
|--------|----------|---------|
| `setup.sh` | Unix | Environment setup & initialization |
| `run_pipeline.sh` | Unix | One-click pipeline execution |
| `run_pipeline.bat` | Windows | One-click pipeline execution |
| `tests/run_test.sh` | Unix | Run full test suite |
| `tests/run_test.bat` | Windows | Run full test suite |

### Data

| File | Purpose | Format |
|------|---------|--------|
| `documents.txt` | Input data | Plain text, semi-structured |
| `output/entities/entities_output.json` | Entity extraction output | JSON |
| `output/relations/relations_output.json` | Relation extraction output | JSON |
| `output/evaluation/evaluation_report.json` | Evaluation results | JSON |

## 🎯 Common Tasks

### Task 1: Extract Entities Only

```bash
python -c "
from entity_extractor import extract_entities
extract_entities('documents.txt', 'output/entities/entities_output.json')
"
```

Or programmatically:
```python
from entity_extractor import EntityExtractor

extractor = EntityExtractor()
entities = extractor.extract_from_file('documents.txt')
extractor.save_results('output/entities/entities_output.json')
```

### Task 2: Extract Relations Only

```bash
python -c "
from relation_extractor import extract_relations
extract_relations('documents.txt', 'output/entities/entities_output.json', 'output/relations/relations_output.json')
"
```

Or programmatically:
```python
from relation_extractor import RelationExtractor

extractor = RelationExtractor()
relations = extractor.extract_from_file('documents.txt', 'output/entities/entities_output.json')
extractor.save_results('output/relations/relations_output.json')
```

### Task 3: Run Complete Pipeline

```bash
python main.py --input documents.txt --method "My-Method"
```

Or:
```bash
bash run_pipeline.sh  # Unix
run_pipeline.bat      # Windows
```

### Task 4: Run Tests

```bash
bash tests/run_test.sh        # Unix - full suite
tests\run_test.bat            # Windows - full suite
pytest tests/test_kgeb.py -v  # Specific tests
```

### Task 5: Add New Entity Type

1. Edit `entities.json`: Add entity type and attributes
2. Edit `entity_extractor.py`: Add extraction pattern
3. Add test in `tests/test_kgeb.py`
4. Run tests to verify

See `DEVELOPER.md` → "Adding a New Entity Type" for details.

### Task 6: Add New Relation Type

1. Edit `relations.json`: Add relation definition
2. Edit `relation_extractor.py`: Add extraction pattern
3. Add test in `tests/test_kgeb.py`
4. Run tests to verify

See `DEVELOPER.md` → "Adding a New Relation Type" for details.

### Task 7: Customize Configuration

See `CONFIGURATION.md` for all available options:
- Entity schema customization
- Relation schema customization
- Pipeline configuration
- Extraction patterns
- Evaluation thresholds

### Task 8: Run in Docker

```bash
# Build
docker build -t kgeb:latest .

# Run
docker run -v $(pwd)/output:/app/output kgeb:latest

# Custom input
docker run -v $(pwd)/data:/app/data -v $(pwd)/output:/app/output kgeb:latest \
  python main.py --input data/documents.txt
```

### Task 9: Generate Test Reports

```bash
# Full report with coverage
bash tests/run_test.sh

# Specific test category reports
pytest tests/test_kgeb.py::TestReproducibility -v
pytest tests/test_kgeb.py::TestPersistence -v
pytest tests/test_kgeb.py::TestMultiDocument -v
```

Reports generated in `reports/` directory.

### Task 10: Create Custom Evaluation Report

```python
from test_report_templates import ComprehensiveTestReportTemplate

report = ComprehensiveTestReportTemplate.create_report(
    reproducibility={...},
    persistence={...},
    conflict_handling={...},
    multi_document={...},
    schema_compliance={...},
    integration={...}
)

ComprehensiveTestReportTemplate.save_report(report, 'reports/custom_report.json')
ComprehensiveTestReportTemplate.print_report_summary(report)
```

## 📊 Data Flow

```
Input Documents (documents.txt)
           ↓
    [Entity Extraction]
           ↓
Entities (entities_output.json)
           ↓
    [Relation Extraction] ← Uses entities
           ↓
Relations (relations_output.json)
           ↓
    [Evaluation]
           ↓
Report (evaluation_report.json)
```

## 🔧 Configuration Quick Reference

### Pipeline Options

```bash
python main.py \
  --input documents.txt          # Input file
  --output-dir output            # Output directory
  --data-dir .                   # Data directory
  --method "Method-Name"         # Method identifier
  --entities-schema entities.json # Entity schema path
  --relations-schema relations.json # Relation schema path
```

### Test Options

```bash
pytest tests/test_kgeb.py -v           # Verbose output
pytest tests/test_kgeb.py --tb=short   # Short traceback
pytest tests/test_kgeb.py -k TestName  # Specific test
pytest tests/ --cov=. --cov-report=html  # Coverage report
```

## 📈 Metrics Reference

### Entity Extraction Metrics

- **Precision**: Correctly extracted / Total extracted (0-1)
- **Recall**: Correctly extracted / Total gold (0-1)
- **F1 Score**: Harmonic mean of precision & recall (0-1)
- **Schema Compliance**: % complying with schema (0-100%)

### Relation Extraction Metrics

- **Precision**: Correct relations / Total extracted (0-1)
- **Recall**: Correct relations / Total gold (0-1)
- **F1 Score**: Harmonic mean (0-1)
- **Consistency Score**: Logical consistency (0-1)

## 🧪 Test Categories

1. **Reproducibility Tests**: Same input → same output
2. **Persistence Tests**: Save/load functionality
3. **Conflict Handling Tests**: Duplicate detection
4. **Multi-Document Tests**: Multi-file processing
5. **Schema Compliance Tests**: Schema validation
6. **Integration Tests**: Full pipeline tests

## 📝 Entity & Relation Types

### 10 Entity Types
- Person, Company, Project
- Department, Position, Technology
- Location, Team, Product
- Client

### 30+ Relation Types
- BelongsTo, ManagesProject, WorksAt
- HasPosition, LocatedIn, OwnsProject
- OperatesIn, HasDepartment, UsesTechnology
- ProducesProduct, HasTeam, PersonInTeam
- TeamFocusArea, ClientContract, ClientUses
- ProjectInvolves, ProjectStatus, DepartmentHead
- ProductVersion, TechnologyVersion, CompanyPartnership
- PersonMentor, OfficeType, ProjectTimeline
- EmployeeCount, SalaryRange, ProjectBudget
- IndustryCategory, LocationCountry, PersonAge
- CollaborationOn, And more...

## 🚀 Performance Tips

1. **For Large Documents**: Process in chunks
2. **For Relation Extraction**: Pre-index entities
3. **For Batch Processing**: Use loop with results aggregation
4. **For Memory**: Stream processing instead of loading all

## 🐛 Troubleshooting Quick Guide

| Issue | Solution | Reference |
|-------|----------|-----------|
| Entities not found | Check patterns in entity_extractor.py | CONFIGURATION.md |
| Relations empty | Verify entity lookup logic | DEVELOPER.md |
| Schema validation fails | Check required attributes | CONFIGURATION.md |
| Low F1 scores | Review patterns and adjust | DEVELOPER.md |
| Tests failing | Run individual test, check output | tests/test_kgeb.py |
| Docker build fails | Check Python version and dependencies | Dockerfile |

## 🔍 API Quick Reference

### EntityExtractor

```python
extractor = EntityExtractor()
entities = extractor.extract_from_text(text)
entities = extractor.extract_from_file(filepath)
extractor.save_results(output_path)
stats = extractor.get_statistics()
```

### RelationExtractor

```python
extractor = RelationExtractor()
relations = extractor.extract_from_text(text, entities)
relations = extractor.extract_from_file(text_file, entities_file)
extractor.save_results(output_path)
stats = extractor.get_statistics()
```

### EntityEvaluator

```python
metrics = EntityEvaluator.calculate_metrics(gold_entities, predicted_entities)
```

### RelationEvaluator

```python
metrics = RelationEvaluator.calculate_metrics(gold_relations, predicted_relations)
```

### KGEBPipeline

```python
pipeline = KGEBPipeline(data_dir, output_dir)
results = pipeline.run_full_pipeline(input_file, method_name)
```

## 📞 Contact & Support

For questions or issues:
1. Check README.md first
2. Review CONFIGURATION.md for options
3. Check DEVELOPER.md for implementation details
4. Review relevant source code docstrings
5. Check test examples in tests/test_kgeb.py

---

**Last Updated**: November 7, 2025
**KGEB Version**: 1.0.0
**Status**: ✅ Complete and Tested
