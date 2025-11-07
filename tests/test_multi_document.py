from pathlib import Path
from kgeb.extractors import extract_entities


def test_multi_document_merge():
    docs = [
        "Alice Q, age 30, works at Wonderland as a Developer.",
        "Alice Q, age 31, works at Wonderland as a Developer.",
        "Bob Q, age 40, works at Wonderland as a Manager."
    ]
    schema = {"Person": ["name", "age", "position", "department"], "Company": ["name", "industry", "sector", "location"]}
    entities = extract_entities(docs, schema)
    # Ensure that two lines with same person name get merged -> only one record per unique name
    assert any(p.get("name") == "Alice Q" for p in entities["Person"]) 
    # There should not be two distinct entries with same name
    assert sum(1 for p in entities["Person"] if p.get("name") == "Alice Q") <= 1
