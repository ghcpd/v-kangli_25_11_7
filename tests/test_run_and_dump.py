import json
import os
from pathlib import Path
from kgeb.config import load_documents, load_entities_schema, load_relations_schema
from kgeb.extractors import extract_entities, extract_relations

ROOT = Path(__file__).resolve().parent.parent

def test_run_and_dump(tmp_path):
    docs = load_documents()
    schema = load_entities_schema()
    rel_schema = load_relations_schema()

    entities = extract_entities(docs, schema)
    relations = extract_relations(docs, schema, rel_schema)

    out_e = tmp_path / "entities_output.json"
    out_r = tmp_path / "relations_output.json"
    with open(out_e, "w", encoding="utf-8") as f:
        json.dump(entities, f, indent=2, ensure_ascii=False)
    with open(out_r, "w", encoding="utf-8") as f:
        json.dump(relations, f, indent=2, ensure_ascii=False)

    assert out_e.exists()
    assert out_r.exists()
    # ensure we have at least some entries
    assert len(entities.get("Person", [])) > 0
    assert len(relations.get("WorksAt", [])) > 0
