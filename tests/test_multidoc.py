from src.loader import load_documents
from src.extractor import extract_entities_from_text
from src.schemas import load_entities_schema


def test_deduplicate_across_documents(tmp_path, monkeypatch):
    schema = load_entities_schema('entities.json')
    d1 = 'John Zhang works in R&D department.'
    d2 = 'John Zhang, age 35, joined project X.'
    docs = [d1, d2]
    # extract independently and merge
    ent_all = {k: [] for k in schema}
    for d in docs:
        ent = extract_entities_from_text(d, schema)
        for k, v in ent.items():
            ent_all[k].extend(v)
    # dedupe
    names = [p.get('name') for p in ent_all['Person']]
    assert len(names) == len(set(names))
