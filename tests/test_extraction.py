import json
from pathlib import Path
from kgeb.config import load_documents, load_entities_schema, load_relations_schema
from kgeb.extractors import extract_entities, extract_relations
from kgeb.evaluator import evaluate_entities, evaluate_relations, generate_evaluation_report

ROOT = Path(__file__).resolve().parent.parent

def test_extraction_run(tmp_path):
    docs = load_documents(ROOT / "documents.txt") if (ROOT / "documents.txt").exists() else load_documents()
    schema = load_entities_schema(ROOT / "entities.json")
    rel_schema = load_relations_schema(ROOT / "relations.json")

    entities = extract_entities(docs, schema)
    relations = extract_relations(docs, schema, rel_schema)

    # basic assertions: entities and relations not empty for this corpus
    assert isinstance(entities, dict)
    assert isinstance(relations, dict)
    assert len(entities.get("Person", [])) > 0
    assert len(entities.get("Company", [])) > 0
    assert len(relations.get("WorksAt", [])) > 0

    # schema compliance check
    eval_entities = evaluate_entities(entities)
    assert "schema_compliance" in eval_entities

    eval_relations = evaluate_relations(relations, entities=entities)
    assert "logical_consistency" in eval_relations

    report = generate_evaluation_report(eval_entities, eval_relations, method_name="TestBaseline", out_path=tmp_path / "report.json")
    assert report["method"] == "TestBaseline"
    assert "conflicts" in report

