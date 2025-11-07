from pathlib import Path
from evaluator import evaluate_entities, evaluate_relations


def test_evaluation_basics():
    repo_root = Path(__file__).resolve().parents[1]
    pred_ent = repo_root / 'tests' / 'data' / 'gold_entities.json'
    gold_ent = repo_root / 'tests' / 'data' / 'gold_entities.json'
    pred_rel = repo_root / 'tests' / 'data' / 'gold_relations.json'
    gold_rel = repo_root / 'tests' / 'data' / 'gold_relations.json'

    ent_res = evaluate_entities(str(pred_ent), str(gold_ent))
    rel_res = evaluate_relations(str(pred_rel), str(gold_rel))
    assert '_aggregate' in ent_res
    assert '_aggregate' in rel_res
    assert 0.0 <= ent_res['_aggregate']['f1'] <= 1.0
    assert 0.0 <= rel_res['_aggregate']['f1'] <= 1.0


if __name__ == '__main__':
    test_evaluation_basics()
    print('Evaluation test ran successfully')
