import json
from collections import defaultdict


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def flatten_entities(entities):
    flat = []
    for etype, items in entities.items():
        for it in items:
            flat.append((etype, json.dumps(it, sort_keys=True)))
    return set(flat)


def compute_prf(gold_set, pred_set):
    tp = len(gold_set & pred_set)
    fp = len(pred_set - gold_set)
    fn = len(gold_set - pred_set)
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    return precision, recall, f1


def schema_compliance(entities, schema):
    total = 0
    compliant = 0
    for etype, items in entities.items():
        required = set(schema.get(etype, []))
        for it in items:
            total += 1
            if required.issubset(set(it.keys())):
                compliant += 1
    return round(compliant / total * 100, 2) if total else 0.0


if __name__ == '__main__':
    import argparse, datetime
    parser = argparse.ArgumentParser()
    parser.add_argument('--gold', default='gold_entities.json')
    parser.add_argument('--pred', default='../entities_output.json')
    parser.add_argument('--schema', default='../entities.json')
    parser.add_argument('--out', default='../evaluation_report.json')
    args = parser.parse_args()

    gold = load_json(args.gold)
    pred = load_json(args.pred)
    schema = load_json(args.schema)

    gold_set = flatten_entities(gold)
    pred_set = flatten_entities(pred)

    p, r, f1 = compute_prf(gold_set, pred_set)
    compliance = schema_compliance(pred, schema)

    report = {
        'method': 'Baseline-RuleBased',
        'entity_precision': round(p, 3),
        'entity_recall': round(r, 3),
        'entity_f1': round(f1, 3),
        'schema_compliance': f"{compliance}%",
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z'
    }

    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    print('Evaluation written to', args.out)
