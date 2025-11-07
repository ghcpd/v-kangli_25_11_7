import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_entities_schema(path: Path = None):
    if path is None:
        path = ROOT / "entities.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_relations_schema(path: Path = None):
    if path is None:
        path = ROOT / "relations.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_documents(path: Path = None):
    if path is None:
        path = ROOT / "documents.txt"
    with open(path, "r", encoding="utf-8") as f:
        return f.read().splitlines()
