import json
from typing import Dict, List, Any
from collections import Counter
from datetime import datetime

def precision_recall_f1(pred: List[Dict[str, Any]], gold: List[Dict[str, Any]]) -> Dict[str, float]:
    # simple exact-match on JSON-serializable dicts
    pred_set = [json.dumps(p, sort_keys=True) for p in pred]
    gold_set = [json.dumps(g, sort_keys=True) for g in gold]
    pred_counter = Counter(pred_set)
    gold_counter = Counter(gold_set)

    tp = sum((pred_counter & gold_counter).values())
    fp = sum((pred_counter - gold_counter).values())
    fn = sum((gold_counter - pred_counter).values())

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    return {"precision": precision, "recall": recall, "f1": f1}

def schema_compliance(pred_entities: Dict[str, List[Dict[str, Any]]], schema: Dict[str, List[str]]) -> float:
    total = 0
    compliant = 0
    for etype, items in pred_entities.items():
        expected_fields = set(schema.get(etype, []))
        for item in items:
            total += 1
            if expected_fields.issuperset(item.keys()):
                compliant += 1
    return (compliant / total * 100.0) if total > 0 else 100.0

def evaluate_all(method_name: str, pred_entities: Dict[str, List[Dict[str, Any]]], gold_entities: Dict[str, List[Dict[str, Any]]], schema: Dict[str, List[str]], pred_relations: Dict[str, List[Dict[str, Any]]], gold_relations: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
    # compute entity-level F1 by flattening across types
    all_pred = []
    all_gold = []
    for etype in set(list(pred_entities.keys()) + list(gold_entities.keys())):
        all_pred.extend(pred_entities.get(etype, []))
        all_gold.extend(gold_entities.get(etype, []))

    ent_metrics = precision_recall_f1(all_pred, all_gold)

    all_pred_rel = []
    all_gold_rel = []
    for rtype in set(list(pred_relations.keys()) + list(gold_relations.keys())):
        all_pred_rel.extend(pred_relations.get(rtype, []))
        all_gold_rel.extend(gold_relations.get(rtype, []))

    rel_metrics = precision_recall_f1(all_pred_rel, all_gold_rel)

    compliance = schema_compliance(pred_entities, schema)

    report = {
        "method": method_name,
        "entity_precision": ent_metrics["precision"],
        "entity_recall": ent_metrics["recall"],
        "entity_f1": ent_metrics["f1"],
        "relation_precision": rel_metrics["precision"],
        "relation_recall": rel_metrics["recall"],
        "relation_f1": rel_metrics["f1"],
        "schema_compliance": f"{compliance:.1f}%",
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

    return report
