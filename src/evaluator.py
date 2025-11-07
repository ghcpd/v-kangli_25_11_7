"""
Evaluation utilities for KGEB baseline.
"""
import json
from typing import Dict, Any, List, Tuple
from collections import defaultdict


def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def compute_prf(pred: List[Any], gold: List[Any]) -> Tuple[float, float, float]:
    # Use simple exact matching for PRF
    pred_set = {json.dumps(p, sort_keys=True) for p in pred}
    gold_set = {json.dumps(g, sort_keys=True) for g in gold}
    tp = len(pred_set & gold_set)
    fp = len(pred_set - gold_set)
    fn = len(gold_set - pred_set)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0
    return precision, recall, f1


def evaluate_entities(pred_path: str, gold_path: str) -> Dict[str, Any]:
    pred = load_json(pred_path)
    gold = load_json(gold_path)
    results = {}
    all_tp = all_fp = all_fn = 0
    for ent_type in set(list(pred.keys()) + list(gold.keys())):
        p_list = pred.get(ent_type, [])
        g_list = gold.get(ent_type, [])
        precision, recall, f1 = compute_prf(p_list, g_list)
        results[ent_type] = {"precision": precision, "recall": recall, "f1": f1, "predicted": len(p_list), "gold": len(g_list)}
        # accumulate for macro-average - simple sum
        all_tp += len({json.dumps(p, sort_keys=True) for p in p_list} & {json.dumps(g, sort_keys=True) for g in g_list})
        all_fp += max(0, len(p_list) - len({json.dumps(p, sort_keys=True) for p in p_list} & {json.dumps(g, sort_keys=True) for g in g_list}))
        all_fn += max(0, len(g_list) - len({json.dumps(p, sort_keys=True) for p in p_list} & {json.dumps(g, sort_keys=True) for g in g_list}))
    precision = all_tp / (all_tp + all_fp) if (all_tp + all_fp) > 0 else 0.0
    recall = all_tp / (all_tp + all_fn) if (all_tp + all_fn) > 0 else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0
    results["_aggregate"] = {"precision": precision, "recall": recall, "f1": f1}
    return results


def evaluate_relations(pred_path: str, gold_path: str) -> Dict[str, Any]:
    pred = load_json(pred_path)
    gold = load_json(gold_path)
    results = {}
    all_tp = all_fp = all_fn = 0
    for rel_type in set(list(pred.keys()) + list(gold.keys())):
        p_list = pred.get(rel_type, [])
        g_list = gold.get(rel_type, [])
        precision, recall, f1 = compute_prf(p_list, g_list)
        results[rel_type] = {"precision": precision, "recall": recall, "f1": f1, "predicted": len(p_list), "gold": len(g_list)}
        all_tp += len({json.dumps(p, sort_keys=True) for p in p_list} & {json.dumps(g, sort_keys=True) for g in g_list})
        all_fp += max(0, len(p_list) - len({json.dumps(p, sort_keys=True) for p in p_list} & {json.dumps(g, sort_keys=True) for g in g_list}))
        all_fn += max(0, len(g_list) - len({json.dumps(p, sort_keys=True) for p in p_list} & {json.dumps(g, sort_keys=True) for g in g_list}))
    precision = all_tp / (all_tp + all_fp) if (all_tp + all_fp) > 0 else 0.0
    recall = all_tp / (all_tp + all_fn) if (all_tp + all_fn) > 0 else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0
    results["_aggregate"] = {"precision": precision, "recall": recall, "f1": f1}
    return results


def schema_compliance(pred_path: str, schema_path: str) -> Dict[str, Any]:
    pred = load_json(pred_path)
    schema = load_json(schema_path)
    compliant = 0
    total = 0
    for ent_type, items in pred.items():
        for item in items:
            total += 1
            # the schema lists allowed fields
            allowed = set(schema.get(ent_type, []))
            if set(item.keys()).issubset(allowed) and set(schema.get(ent_type, [])).issubset(set(item.keys())):
                compliant += 1
    perc = (compliant / total * 100) if total > 0 else 0.0
    return {"compliant": compliant, "total": total, "percentage": perc}


def check_relation_consistency(rel_path: str, entities_path: str) -> Dict[str, Any]:
    rels = load_json(rel_path)
    entities = load_json(entities_path)
    missing = []
    for rel_type, entries in rels.items():
        for e in entries:
            for k, v in e.items():
                if k in ("person", "company", "project", "team", "product", "client"):
                    # simple check: is v present among entities of corresponding type
                    type_map = {"person": "Person", "company": "Company", "project": "Project", "team": "Team", "product": "Product", "client": "Client"}
                    expected_type = type_map.get(k)
                    found = False
                    if expected_type and expected_type in entities:
                        for item in entities[expected_type]:
                            # match by name or project name
                            if item.get("name") == v or item.get("project") == v:
                                found = True
                                break
                    if not found:
                        missing.append({"relation": rel_type, "field": k, "value": v})
    return {"missing_references": missing, "count_missing": len(missing)}

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Evaluate KGEB outputs")
    parser.add_argument("--pred_entities", required=True)
    parser.add_argument("--gold_entities", required=True)
    parser.add_argument("--pred_relations", required=True)
    parser.add_argument("--gold_relations", required=True)
    parser.add_argument("--schema", required=True)
    args = parser.parse_args()

    ent_res = evaluate_entities(args.pred_entities, args.gold_entities)
    rel_res = evaluate_relations(args.pred_relations, args.gold_relations)
    schema_res = schema_compliance(args.pred_entities, args.schema)
    consistency = check_relation_consistency(args.pred_relations, args.pred_entities)

    report = {
        "entity_eval": ent_res,
        "relation_eval": rel_res,
        "schema_compliance": schema_res,
        "consistency": consistency
    }
    print(json.dumps(report, indent=2))
    # Save evaluation report
    with open("evaluation_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print("Saved evaluation report to evaluation_report.json")
