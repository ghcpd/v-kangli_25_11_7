import json
from pathlib import Path


def load_entities_schema(path: str = 'entities.json'):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Schema file not found: {p}")
    with open(p, 'r', encoding='utf-8') as fh:
        return json.load(fh)


def load_relations_schema(path: str = 'relations.json'):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Relations file not found: {p}")
    with open(p, 'r', encoding='utf-8') as fh:
        return json.load(fh)
