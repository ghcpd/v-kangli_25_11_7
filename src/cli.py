import json
import argparse
from pathlib import Path
from .loader import load_documents
from .schemas import load_entities_schema, load_relations_schema
from .extractor import extract_entities_from_text
from .relations import extract_relations_from_text
from .evaluator import evaluate_entities, schema_compliance, relations_consistency, generate_evaluation_report


def merge_entity_lists(lists_of_dicts):
    # just returns all unique by name
    out = []
    seen = set()
    for e in lists_of_dicts:
        key = tuple(sorted((str(v) for v in e.values())))
        if key in seen:
            continue
        seen.add(key)
        out.append(e)
    return out


def main():
    parser = argparse.ArgumentParser(description='KGEB: Entity and Relation extraction benchmark run')
    parser.add_argument('--docs', default='documents.txt')
    parser.add_argument('--entities', default='entities.json')
    parser.add_argument('--relations', default='relations.json')
    parser.add_argument('--gold-entities', default=None)
    parser.add_argument('--gold-relations', default=None)
    parser.add_argument('--out-entities', default='entities_output.json')
    parser.add_argument('--out-relations', default='relations_output.json')
    parser.add_argument('--out-eval', default='evaluation_report.json')
    args = parser.parse_args()

    docs = load_documents(args.docs)
    schema = load_entities_schema(args.entities)
    relations_schema = load_relations_schema(args.relations)

    combined_entities = {k: [] for k in schema}
    combined_relations = {r['name']: [] for r in relations_schema}

    for d in docs:
        ent = extract_entities_from_text(d, schema)
        # merge results into combined
        for k, v in ent.items():
            combined_entities.setdefault(k, []).extend(v)
        rels = extract_relations_from_text(d, ent, relations_schema)
        for k, v in rels.items():
            combined_relations.setdefault(k, []).extend(v)

    # dedupe
    for k in combined_entities:
        combined_entities[k] = merge_entity_lists(combined_entities[k])

    for k in combined_relations:
        combined_relations[k] = merge_entity_lists(combined_relations[k])

    # write
    Path(args.out_entities).write_text(json.dumps(combined_entities, indent=2, ensure_ascii=False))
    Path(args.out_relations).write_text(json.dumps(combined_relations, indent=2, ensure_ascii=False))
    print('Wrote', args.out_entities, args.out_relations)

    # optional evaluation
    if args.gold_entities or args.gold_relations:
        gold_entities = json.loads(Path(args.gold_entities).read_text()) if args.gold_entities else {}
        gold_rel = json.loads(Path(args.gold_relations).read_text()) if args.gold_relations else {}
        ent_eval = evaluate_entities(gold_entities, combined_entities)
        sche = schema_compliance(combined_entities, schema)
        rel_eval = relations_consistency(combined_relations, combined_entities)
        report = generate_evaluation_report('Baseline Heuristics', ent_eval, rel_eval, sche['pct'])
        Path(args.out_eval).write_text(json.dumps(report, indent=2, ensure_ascii=False))
        print('Wrote', args.out_eval)


if __name__ == '__main__':
    main()
