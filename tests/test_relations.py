from src.extractor import extract_entities_from_text
from src.schemas import load_entities_schema
from src.relations import extract_relations_from_text


def test_relation_employee_belongs():
    schema = load_entities_schema('entities.json')
    text = "Lisa Li works as Manager in Marketing department at Alibaba Inc."
    ents = extract_entities_from_text(text, schema)
    rels = extract_relations_from_text(text, ents, __import__('json').load(open('relations.json')))
    assert 'BelongsTo' in rels
    # We expect the department to be linked to the person
    found = rels['BelongsTo']
    assert any('person' in r and 'department' in r for r in found)
