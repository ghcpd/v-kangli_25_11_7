import argparse
import json
from .loader import load_documents, load_json
from .extractor import extract_entities, ENTITY_SCHEMA
from .relation_extractor import extract_relations
from .evaluator import evaluate_all

def run(args):
    print(f"Loading documents from: {args.documents}")
    docs = load_documents(args.documents)
    print(f"Loaded {len(docs)} documents")
    print(f"Loading schema from: {args.entities}")
    schema = load_json(args.entities)
    all_pred_entities = {k: [] for k in schema.keys()}
    all_pred_relations = {}

    for doc in docs:
        ents = extract_entities(doc)
        rels = extract_relations(doc, ents)
        for k, v in ents.items():
            all_pred_entities.setdefault(k, []).extend(v)
        for k, v in rels.items():
            all_pred_relations.setdefault(k, []).extend(v)

    print(f"Writing entities output to: {args.entities_output}")
    with open(args.entities_output, 'w', encoding='utf-8') as f:
        json.dump(all_pred_entities, f, ensure_ascii=False, indent=2)

    print(f"Writing relations output to: {args.relations_output}")
    with open(args.relations_output, 'w', encoding='utf-8') as f:
        json.dump(all_pred_relations, f, ensure_ascii=False, indent=2)

    # if gold provided, run evaluation
    if args.gold_entities and args.gold_relations:
        gold_entities = load_json(args.gold_entities)
        gold_relations = load_json(args.gold_relations)
        report = evaluate_all(args.method or "rule-based", all_pred_entities, gold_entities, schema, all_pred_relations, gold_relations)
        print(f"Writing evaluation report to: {args.evaluation_output}")
        with open(args.evaluation_output, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(json.dumps(report, indent=2))
    else:
        print("Extraction complete. Outputs written.")

def main():
    parser = argparse.ArgumentParser(description='KGEB pipeline runner')
    parser.add_argument('--documents', default='documents.txt')
    parser.add_argument('--entities', default='entities.json')
    parser.add_argument('--entities-output', default='entities_output.json')
    parser.add_argument('--relations-output', default='relations_output.json')
    parser.add_argument('--gold-entities', default='gold_entities.json')
    parser.add_argument('--gold-relations', default='gold_relations.json')
    parser.add_argument('--evaluation-output', default='evaluation_report.json')
    parser.add_argument('--method', default=None)
    args = parser.parse_args()
    run(args)

if __name__ == '__main__':
    main()
