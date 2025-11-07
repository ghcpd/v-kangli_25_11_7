import json
import re
from collections import defaultdict


def load_relations_schema(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_relations(doc_text, schema):
    results = defaultdict(list)
    lines = doc_text.splitlines()

    # Simple relation: "X manages N projects: A, B, C." -> Person manages Projects
    manages_re = re.compile(r"^(?P<name>[A-Z][a-z]+(?: [A-Z][a-z]+)+) manages (?:\d+ )?projects:\s*(?P<projects>.+)\.")

    for line in lines:
        m = manages_re.match(line.strip())
        if m:
            name = m.group('name')
            projs = [p.strip() for p in m.group('projects').split(',')]
            for p in projs:
                results['ManagesProject'].append({'person': name, 'project': p})

    # Works at -> Employment relation
    works_re = re.compile(r"^(?P<name>[A-Z][a-z]+(?: [A-Z][a-z]+)+), age (?P<age>\d+), works at (?P<company>[A-Za-z0-9 &-]+) as a? (?P<position>.+)\.")
    for line in lines:
        m = works_re.match(line.strip())
        if m:
            d = m.groupdict()
            results['EmployedBy'].append({'person': d['name'], 'company': d['company'], 'position': d['position']})

    return results


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='KGEB simple relation extractor')
    parser.add_argument('--docs', default='../documents.txt')
    parser.add_argument('--relations', default='../relations.json')
    parser.add_argument('--out', default='../relations_output.json')
    args = parser.parse_args()

    with open(args.docs, 'r', encoding='utf-8') as f:
        docs = f.read()
    schema = load_relations_schema(args.relations)
    rels = extract_relations(docs, schema)
    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(rels, f, indent=2)
    print('Relations extracted:', sum(len(v) for v in rels.values()))
