import json
import re
from collections import defaultdict

# Basic rule-based extractor for demonstration purposes

def load_entities_schema(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_entities(doc_text, schema):
    results = defaultdict(list)
    lines = doc_text.splitlines()

    # Simple person extraction: Name, age, works at Company as Position
    person_re = re.compile(r"^(?P<name>[A-Z][a-z]+(?: [A-Z][a-z]+)+), age (?P<age>\d+), works at (?P<company>[A-Za-z0-9 &-]+) as a? (?P<position>[A-Za-z0-9 \-/]+)\.")

    for line in lines:
        m = person_re.match(line.strip())
        if m:
            p = m.groupdict()
            person = {k: p.get('name'), 'age': int(p.get('age')), 'position': p.get('position'), 'department': None}
            results['Person'].append(person)
            # add company entity
            results['Company'].append({'name': p.get('company'), 'industry': None, 'sector': None, 'location': None})

        # project lines (very naive)
        if line.lower().startswith('project '):
            # Project Name started on YYYY-MM-DD, ends on YYYY-MM-DD
            parts = re.split(r"[:,] ", line)
            name = parts[0].replace('Project ', '').strip()
            dates = re.findall(r"(\d{4}-\d{2}-\d{2})", line)
            proj = {'name': name, 'start_date': dates[0] if dates else None, 'end_date': dates[1] if len(dates) > 1 else None, 'status': None, 'budget': None}
            results['Project'].append(proj)

        # company industry lines
        if ' operates ' in line or ' specializes ' in line or ' focuses in ' in line or ' works in ' in line:
            # company operates in the X industry
            comp_m = re.match(r"(?P<company>[A-Za-z0-9 &-]+) (?:operates|specializes|focuses|works) in(?: the)? (?P<industry>.+?) industry\.", line)
            if comp_m:
                c = comp_m.groupdict()
                results['Company'].append({'name': c['company'], 'industry': c['industry'], 'sector': None, 'location': None})

    # Deduplicate by name per entity
    for etype, items in list(results.items()):
        seen = {}
        unique = []
        for it in items:
            key = it.get('name') or it.get('title')
            if key and key not in seen:
                seen[key] = True
                unique.append(it)
        results[etype] = unique

    return results


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='KGEB simple extractor')
    parser.add_argument('--docs', default='../documents.txt')
    parser.add_argument('--entities', default='../entities.json')
    parser.add_argument('--out', default='../entities_output.json')
    args = parser.parse_args()

    with open(args.docs, 'r', encoding='utf-8') as f:
        docs = f.read()
    schema = load_entities_schema(args.entities)
    entities = extract_entities(docs, schema)
    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(entities, f, indent=2)
    print('Entities extracted:', sum(len(v) for v in entities.values()))
