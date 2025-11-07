# KGEB - 5-Minute Quick Start

## For Impatient Users: Get Running in 5 Minutes

### Step 1: Setup (1 minute)

**On Linux/macOS:**
```bash
bash setup.sh
```

**On Windows:**
```bash
# (requires Python 3.8+ and git installed)
python -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt
```

### Step 2: Run Pipeline (1 minute)

**On Linux/macOS:**
```bash
bash run_pipeline.sh
```

**On Windows:**
```bash
run_pipeline.bat
```

### Step 3: Check Results (1 minute)

Results are in the `output/` directory:

```
output/
├── entities/
│   └── entities_output.json     ← Extracted entities
├── relations/
│   └── relations_output.json    ← Extracted relations
└── evaluation/
    └── evaluation_report.json   ← Evaluation metrics
```

### Step 4: Review Outputs (2 minutes)

View with any JSON viewer or:

**Linux/macOS:**
```bash
cat output/entities/entities_output.json | jq .
```

**Windows:**
```bash
type output\entities\entities_output.json
```

---

## What Just Happened?

1. ✅ Extracted 10 types of entities from documents.txt
2. ✅ Extracted 30+ types of relations between entities
3. ✅ Calculated evaluation metrics (Precision, Recall, F1)
4. ✅ Generated comprehensive report

---

## Next Steps

### Want to Run Tests?

```bash
# Linux/macOS
bash tests/run_test.sh

# Windows
tests\run_test.bat
```

### Want to Customize?

1. Edit `documents.txt` with your own data
2. Run pipeline again: `python main.py --input documents.txt`

### Want to Add Custom Entity Type?

1. Edit `entities.json` - add your entity type
2. Edit `entity_extractor.py` - add extraction pattern
3. Run `python main.py --input documents.txt`

### Want Documentation?

- **Quick Reference**: Read `INDEX.md`
- **Configuration Help**: Read `CONFIGURATION.md`
- **Developer Guide**: Read `DEVELOPER.md`
- **Full Details**: Read `README.md`

### Want Docker?

```bash
docker build -t kgeb:latest .
docker run -v $(pwd)/output:/app/output kgeb:latest
```

---

## Command Reference

| Task | Command |
|------|---------|
| Setup environment | `bash setup.sh` |
| Run full pipeline | `bash run_pipeline.sh` |
| Run tests | `bash tests/run_test.sh` |
| Manual pipeline | `python main.py --help` |
| Extract entities only | `python entity_extractor.py` |
| Extract relations only | `python relation_extractor.py` |
| View metrics | `cat output/evaluation/evaluation_report.json` |

---

## Output Files Explained

### entities_output.json
Contains all extracted entities grouped by type:
```json
{
  "Person": [{"name": "...", "age": ..., ...}],
  "Company": [{"name": "...", ...}],
  ...
}
```

### relations_output.json
Contains all extracted relations grouped by type:
```json
{
  "WorksAt": [{"person": "...", "company": "..."}],
  "ManagesProject": [{"person": "...", "project": "..."}],
  ...
}
```

### evaluation_report.json
Contains evaluation metrics:
```json
{
  "method": "KGEB-Baseline",
  "entity_f1": 0.85,
  "relation_f1": 0.78,
  "schema_compliance": "97%",
  "timestamp": "2025-11-07T12:30:00Z"
}
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `command not found: bash` | Use Windows bash shell or WSL |
| Python not found | Install Python 3.8+ |
| Virtual environment won't activate | Check Python path |
| No output files | Check `output/` directory exists |
| Test failures | Run individual test with `-v` flag |

---

## Learning Path

1. **Beginner**: Run quick-start → View outputs → Read README
2. **Intermediate**: Customize configuration → Add entity type → Run tests
3. **Advanced**: Study architecture → Extend framework → Create custom evaluator

---

## All Set! 🚀

You now have a working KGEB system!

- **Documents extracted**: ✓
- **Entities recognized**: ✓
- **Relations identified**: ✓
- **Metrics calculated**: ✓

For more details, see:
- `README.md` - Full documentation
- `INDEX.md` - Quick reference
- `CONFIGURATION.md` - Configuration options
- `DEVELOPER.md` - Extension guide

**Questions?** Check `COMPLETION_REPORT.md` for full project details.
