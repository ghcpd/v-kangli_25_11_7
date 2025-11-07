# Enterprise Knowledge Graph Extraction Benchmark (KGEB)

Lightweight benchmark for entity and relation extraction from semi-structured enterprise text.

Quickstart:

Run extraction locally:

```bash
python -m kgeb.cli --documents documents.txt --entities entities.json
```

Run full test (with gold) to produce `evaluation_report.json`:

```bash
python -m kgeb.cli --documents documents.txt --entities entities.json --gold-entities gold_entities.json --gold-relations gold_relations.json
```

Artifacts:
- `entities_output.json` — extracted entities
- `relations_output.json` — extracted relations
- `evaluation_report.json` — evaluation metrics
# v-kangli_25_11_7