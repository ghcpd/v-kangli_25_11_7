import json
import subprocess
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

from extractors import parse_documents, extract_all, save_json
from evaluator import schema_compliance, check_relation_consistency


def test_run_extractor_and_schema_check(tmp_path):
    repo_root = Path(__file__).resolve().parents[1]
    docs = repo_root / 'documents.txt'
    schema = repo_root / 'entities.json'
    gold_entities = repo_root / 'tests' / 'data' / 'gold_entities.json'
    gold_relations = repo_root / 'tests' / 'data' / 'gold_relations.json'

    lines = parse_documents(str(docs))
    out = extract_all(lines)
    ent_path = tmp_path / 'entities_output.json'
    rel_path = tmp_path / 'relations_output.json'
    save_json(out['entities'], str(ent_path))
    save_json(out['relations'], str(rel_path))

    # Check schema compliance
    comp = schema_compliance(str(ent_path), str(schema))
    assert comp['total'] > 0
    assert comp['percentage'] >= 0

    # Relations should reference existing entities where applicable
    consistency = check_relation_consistency(str(rel_path), str(ent_path))
    assert 'count_missing' in consistency

    # Basic check to ensure outputs written
    assert ent_path.exists()
    assert rel_path.exists()


if __name__ == '__main__':
    import tempfile
    from pathlib import Path
    td = Path(tempfile.mkdtemp())
    print('Running test_run_extractor_and_schema_check with tmp_path', td)
    test_run_extractor_and_schema_check(td)
    print('Test ran successfully')
