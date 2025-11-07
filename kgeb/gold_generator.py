import json
from pathlib import Path
from .config import load_documents, load_entities_schema, load_relations_schema
from .extractors import extract_entities, extract_relations

ROOT = Path(__file__).resolve().parent.parent

def generate_gold(out_entities: Path = None, out_relations: Path = None):
    if out_entities is None:
        out_entities = ROOT / "entities_gold.json"
    if out_relations is None:
        out_relations = ROOT / "relations_gold.json"

    docs = load_documents()
    schema = load_entities_schema()
    rel_schema = load_relations_schema()

    # For the gold generator, we use the baseline extractor but then we filter to only entries that have non-null names and at least 2 attributes present
    entities = extract_entities(docs, schema)
    relations = extract_relations(docs, schema, rel_schema)

    # filter entities for gold
    gold_entities = {}
    for etype, items in entities.items():
        gold_entities[etype] = [i for i in items if i.get("name")]

    # write out
    with open(out_entities, "w", encoding="utf-8") as f:
        json.dump(gold_entities, f, indent=2, ensure_ascii=False)
    with open(out_relations, "w", encoding="utf-8") as f:
        json.dump(relations, f, indent=2, ensure_ascii=False)
    print(f"Wrote {out_entities} and {out_relations}")

if __name__ == "__main__":
    generate_gold()
