from src.extractor import extract_entities_from_text
from src.schemas import load_entities_schema


def test_extract_person_and_company():
    schema = load_entities_schema('entities.json')
    text = "John Zhang, 35 years old, works as Engineer in R&D department of Tencent Inc. Project: Smart City Construction started 2024-01-01 with budget $5,000,000."
    res = extract_entities_from_text(text, schema)
    assert 'Person' in res and len(res['Person']) >= 1
    assert any(p['name'].startswith('John Zhang') for p in res['Person'])
    assert 'Company' in res and any('Tencent' in (c.get('name') or '') for c in res['Company'])
    assert 'Project' in res and any('Smart City Construction' in (p.get('name') or '') for p in res['Project'])
