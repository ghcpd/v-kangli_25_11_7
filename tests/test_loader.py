from src.loader import load_documents


def test_load_documents_exists():
    docs = load_documents('documents.txt')
    assert isinstance(docs, list)
    assert len(docs) >= 1
