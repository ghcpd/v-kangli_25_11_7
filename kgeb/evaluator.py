import json
import datetime
from pathlib import Path
from typing import Dict, List, Any, Tuple
from .config import load_entities_schema, load_relations_schema

ROOT = Path(__file__).resolve().parent.parent


def _safe_name(item: Dict[str, Any]) -> str:
    return item.get("name") or ""


def _match_entity_list(predicted: List[Dict[str, Any]], gold: List[Dict[str, Any]], key: str = "name") -> Tuple[int, int, int]:
    # Return tp, fp, fn counts by exact key match
    pred_names = {p.get(key): p for p in predicted if p.get(key)}
    gold_names = {g.get(key): g for g in gold if g.get(key)}
    tp = sum(1 for n in pred_names.keys() if n in gold_names)
    fp = sum(1 for n in pred_names.keys() if n not in gold_names)
    fn = sum(1 for n in gold_names.keys() if n not in pred_names)
    return tp, fp, fn


def precision_recall_f1(tp: int, fp: int, fn: int) -> Dict[str, float]:
    precision = tp / (tp + fp) if tp + fp > 0 else 0.0
    recall = tp / (tp + fn) if tp + fn > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall > 0 else 0.0
    return {"precision": precision, "recall": recall, "f1": f1}


def evaluate_entities(pred_entities: Dict[str, List[Dict[str, Any]]], gold_path: Path = None) -> Dict[str, Any]:
    entities_schema = load_entities_schema()
    results = {"per_entity": {}, "overall": {}}

    if gold_path and gold_path.exists():
        gold_entities = json.load(open(gold_path, "r", encoding="utf-8"))
        # compute metrics
        total_tp = total_fp = total_fn = 0
        for etype, fields in entities_schema.items():
            pred = pred_entities.get(etype, [])
            gold = gold_entities.get(etype, [])
            tp, fp, fn = _match_entity_list(pred, gold, key="name")
            total_tp += tp; total_fp += fp; total_fn += fn
            results["per_entity"][etype] = {"tp": tp, "fp": fp, "fn": fn}
        metrics = precision_recall_f1(total_tp, total_fp, total_fn)
        results["overall"]["entity_precision"] = metrics["precision"]
        results["overall"]["entity_recall"] = metrics["recall"]
        results["overall"]["entity_f1"] = metrics["f1"]
    else:
        # schema compliance: percentage entities having required fields
        counts = {}
        total_ok = 0
        total = 0
        for etype, fields in entities_schema.items():
            pred = pred_entities.get(etype, [])
            okay = 0
            for p in pred:
                if all(field in p for field in fields):
                    okay += 1
            counts[etype] = {"passed": okay, "n": len(pred)}
            total_ok += okay
            total += len(pred)
        results["schema_compliance"] = f"{(total_ok / total * 100) if total > 0 else 0:.2f}%"
        results["details"] = counts

    return results


def evaluate_relations(pred_relations: Dict[str, List[Dict[str, Any]]], gold_path: Path = None, entities: Dict[str, List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    relations_schema = load_relations_schema()
    results = {"per_relation": {}, "overall": {}}

    if gold_path and gold_path.exists():
        gold_relations = json.load(open(gold_path, "r", encoding="utf-8"))
        total_tp = total_fp = total_fn = 0
        for rtype, args in relations_schema.items():
            pred = pred_relations.get(rtype, [])
            gold = gold_relations.get(rtype, [])
            # match by json equality
            pred_set = {json.dumps(x, sort_keys=True) for x in pred}
            gold_set = {json.dumps(x, sort_keys=True) for x in gold}
            tp = len(pred_set & gold_set)
            fp = len(pred_set - gold_set)
            fn = len(gold_set - pred_set)
            total_tp += tp; total_fp += fp; total_fn += fn
            results["per_relation"][rtype] = {"tp": tp, "fp": fp, "fn": fn}
        metrics = precision_recall_f1(total_tp, total_fp, total_fn)
        results["overall"]["relation_precision"] = metrics["precision"]
        results["overall"]["relation_recall"] = metrics["recall"]
        results["overall"]["relation_f1"] = metrics["f1"]
    else:
        # logical consistency: referenced entities must appear in predicted entities
        missing_refs = {}
        total_refs = 0
        missing = 0
        for rtype, rels in pred_relations.items():
            for r in rels:
                total_refs += 1
                for k, v in r.items():
                    # if the value is an entity name, check it exists in entities
                    if isinstance(v, str) and entities is not None:
                        etype_candidates = [k for k, _ in entities.items()]
                        found = False
                        # look up by name in every entity type
                        for etype, items in entities.items():
                            if any(it.get("name") == v for it in items):
                                found = True
                                break
                        if not found:
                            missing += 1
                            missing_refs.setdefault(rtype, []).append({k: v})
        results["logical_consistency"] = {"total_references": total_refs, "missing_references": missing}
        results["missing_details"] = missing_refs
        # schema compliance for relations: ensure the keys match expected args
        compliance = {}
        for rtype, args in relations_schema.items():
            rels = pred_relations.get(rtype, [])
            ok = 0
            for r in rels:
                if all(k in r for k in args if args):
                    ok += 1
            compliance[rtype] = {"passed": ok, "n": len(rels)}
        results["schema_compliance"] = compliance

    return results


def detect_entity_conflicts(pred_entities: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
    """Detect conflicts within an entity type where the same named entity has conflicting attribute values."""
    conflicts = {}
    for etype, items in pred_entities.items():
        by_name = {}
        for it in items:
            name = it.get("name")
            if not name:
                continue
            if name not in by_name:
                by_name[name] = it.copy()
            else:
                # compare values
                for k, v in it.items():
                    existing = by_name[name].get(k)
                    if existing and v and existing != v:
                        conflicts.setdefault(etype, {}).setdefault(name, []).append({"field": k, "existing": existing, "new": v})
    return conflicts


# modify generate_evaluation_report to include conflicts if found

def generate_evaluation_report(entities_eval: Dict[str, Any], relations_eval: Dict[str, Any], method_name: str = "Baseline", out_path: Path = None):
    # forward compat to include conflicts
    if out_path is None:
        out_path = ROOT / "evaluation_report.json"
    report = {"method": method_name, "timestamp": datetime.datetime.utcnow().isoformat() + "Z"}
    report.update(entities_eval)
    report.update(relations_eval)
    report["conflicts"] = detect_entity_conflicts(entities_eval.get("predicted_entities", {})) if entities_eval.get("predicted_entities") else {}
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    return report


if __name__ == "__main__":
    # run evaluation on outputs
    pred_e_path = ROOT / "entities_output.json"
    pred_r_path = ROOT / "relations_output.json"
    pred_entities = json.load(open(pred_e_path, "r", encoding="utf-8")) if pred_e_path.exists() else {}
    pred_relations = json.load(open(pred_r_path, "r", encoding="utf-8")) if pred_r_path.exists() else {}
    entities_eval = evaluate_entities(pred_entities)
    # include predicted entities in the eval dict for conflict detection
    entities_eval["predicted_entities"] = pred_entities
    relations_eval = evaluate_relations(pred_relations, entities=pred_entities)
    report = generate_evaluation_report(entities_eval, relations_eval, method_name="Baseline")
    print("Evaluation done. Report: Wrote evaluation_report.json")
