import json
from pathlib import Path
from kgeb.config import load_documents, load_entities_schema, load_relations_schema
from kgeb.extractors import extract_entities, extract_relations

ROOT = Path(__file__).resolve().parent

if __name__ == "__main__":
    docs = load_documents()
    schema = load_entities_schema()
    rel_schema = load_relations_schema()

    entities = extract_entities(docs, schema)
    relations = extract_relations(docs, schema, rel_schema)

    out_e = ROOT / "entities_output.json"
    out_r = ROOT / "relations_output.json"
    with open(out_e, "w", encoding="utf-8") as f:
        json.dump(entities, f, indent=2, ensure_ascii=False)
    with open(out_r, "w", encoding="utf-8") as f:
        json.dump(relations, f, indent=2, ensure_ascii=False)

    print("--- ENTITIES summary ---")
    for etype, items in entities.items():
        print(f"{etype}: {len(items)}")
    print("\n--- RELATIONS summary ---")
    for rtype, items in relations.items():
        print(f"{rtype}: {len(items)}")

    # print small sample
    import sys
    print("\nSample Person:\n", json.dumps(entities.get("Person", [])[:3], indent=2, ensure_ascii=False))
    print("\nSample WorksAt relations:\n", json.dumps(relations.get("WorksAt", [])[:5], indent=2, ensure_ascii=False))
