import json
from pathlib import Path
from typing import Dict, List

def load_documents(path: str) -> List[str]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Documents file not found: {path}")
    with p.open(encoding="utf-8") as f:
        # assume each record is separated by a blank line
        content = f.read().strip()
        records = [r.strip() for r in content.split('\n\n') if r.strip()]
    return records

def load_json(path: str) -> Dict:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"JSON file not found: {path}")
    with p.open(encoding="utf-8") as f:
        return json.load(f)
