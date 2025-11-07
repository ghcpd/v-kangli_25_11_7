from kgeb.config import load_documents, load_entities_schema, load_relations_schema
from kgeb.extractors import extract_entities, extract_relations
from kgeb.evaluator import evaluate_entities, evaluate_relations, generate_evaluation_report

if __name__ == "__main__":
    docs = load_documents()
    schema = load_entities_schema()
    rel_schema = load_relations_schema()

    entities = extract_entities(docs, schema)
    relations = extract_relations(docs, schema, rel_schema)

    with open("entities_output.json", "w", encoding="utf-8") as f:
        import json
        json.dump(entities, f, indent=2, ensure_ascii=False)
    with open("relations_output.json", "w", encoding="utf-8") as f:
        import json
        json.dump(relations, f, indent=2, ensure_ascii=False)

    entities_eval = evaluate_entities(entities)
    entities_eval["predicted_entities"] = entities
    relations_eval = evaluate_relations(relations, entities=entities)
    report = generate_evaluation_report(entities_eval, relations_eval, method_name="Baseline")
    print("All done. Wrote outputs and evaluation report.")
