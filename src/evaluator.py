import json
from typing import Dict, List
from collections import Counter
from datetime import datetime


def _match_entity(gold: Dict, pred: Dict):
    # Exact match on 'name' and other non-null attributes
    if gold.get('name') and pred.get('name'):
        if gold['name'].lower() != pred['name'].lower():
            return False
    # Partial match on remaining keys
    for k, v in gold.items():
        if v is None:
            continue
        if pred.get(k) is None:
            return False
        # fuzzy for numbers and dates
        if isinstance(v, str) and v.lower() != str(pred.get(k)).lower():
            return False
        if isinstance(v, (int, float)) and float(v) != float(pred.get(k)):
            return False
    return True


def evaluate_entities(gold: Dict[str, List[Dict]], pred: Dict[str, List[Dict]]):
    stats = {}
    total_tp = total_fp = total_fn = 0
    for ent_type in set(list(gold.keys()) + list(pred.keys())):
        gold_list = gold.get(ent_type, [])
        pred_list = pred.get(ent_type, [])
        tp = 0
        used_pred = set()
        for g in gold_list:
            for i, p in enumerate(pred_list):
                if i in used_pred:
                    continue
                if _match_entity(g, p):
                    tp += 1
                    used_pred.add(i)
                    break
        fp = len(pred_list) - tp
        fn = len(gold_list) - tp
        total_tp += tp; total_fp += fp; total_fn += fn
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0
        stats[ent_type] = {'tp': tp, 'fp': fp, 'fn': fn, 'precision': precision, 'recall': recall, 'f1': f1}
    # micro averaged
    micro_precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0.0
    micro_recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0.0
    micro_f1 = (2 * micro_precision * micro_recall / (micro_precision + micro_recall)) if (micro_precision + micro_recall) > 0 else 0.0
    return {'per_type': stats, 'micro': {'precision': micro_precision, 'recall': micro_recall, 'f1': micro_f1}}


def schema_compliance(pred: Dict[str, List[Dict]], schema: Dict):
    # count how many extracted entities conform to schema (only contain defined attributes)
    total_found = 0
    compliant = 0
    for t, items in pred.items():
        defined = schema.get(t, [])
        for it in items:
            total_found += 1
            # all keys in it must be subset of defined
            if all(k in defined for k in it.keys()):
                compliant += 1
    pct = (compliant / total_found) * 100 if total_found > 0 else 0.0
    return {'total': total_found, 'compliant': compliant, 'pct': pct}


def relations_consistency(relations: Dict[str, List[Dict]], entities: Dict[str, List[Dict]]):
    # Ensure referenced resources exist
    valid = 0
    total = 0
    names = {}
    for t, items in entities.items():
        names.setdefault(t, set())
        for it in items:
            if it.get('name'):
                names[t].add(it.get('name'))
    for rel_name, rels in relations.items():
        for r in rels:
            total += 1
            ok = False
            # check for up to two fields, confirm they exist in entity sets
            if 'person' in r:
                ok = r['person'] in names.get('Person', set())
            if 'department' in r:
                ok = ok and r['department'] in names.get('Department', set()) if ok else r['department'] in names.get('Department', set())
            else:
                # if not person-based, just accept if any value matches
                for v in r.values():
                    for t, s in names.items():
                        if v in s:
                            ok = True
            if ok:
                valid += 1
    pct = (valid / total) * 100 if total > 0 else 0.0
    return {'total': total, 'valid': valid, 'pct': pct}


def generate_evaluation_report(method_name: str, entity_eval: Dict, relation_eval: Dict, schema_pct: float):
    return {
        'method': method_name,
        'entity_precision': entity_eval['micro']['precision'],
        'entity_recall': entity_eval['micro']['recall'],
        'entity_f1': entity_eval['micro']['f1'],
        'relation_consistency_pct': relation_eval.get('pct', 0.0),
        'schema_compliance': f"{schema_pct:.1f}%",
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }

