from pathlib import Path


def load_documents(path: str = 'documents.txt'):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Documents not found: {p}")
    with open(p, 'r', encoding='utf-8') as fh:
        docs = [line.strip() for line in fh if line.strip()]
    return docs
