from typing import Dict, List
import re


def _split_sentences(text: str):
    return re.split(r'[\n\.]', text)


def extract_relations_from_text(text: str, entities: Dict[str, List[Dict]], relations_schema: List[Dict]):
    sentences = _split_sentences(text)
    # index entity names to types
    name_index = {}
    for typ, items in entities.items():
        for it in items:
            name = it.get('name')
            if name:
                name_index.setdefault(name, []).append((typ, it))

    rel_res = {r['name']: [] for r in relations_schema}

    for sent in sentences:
        for rel in relations_schema:
            from_t = rel['from']
            to_t = rel['to']
            # naive: find co-occurring entity names of appropriate types in the sentence
            from_candidates = [it for it in entities.get(from_t, []) if it.get('name') and it.get('name') in sent]
            to_candidates = [it for it in entities.get(to_t, []) if it.get('name') and it.get('name') in sent]
            if from_candidates and to_candidates:
                for f in from_candidates:
                    for t in to_candidates:
                        # map keys generically
                        entry = {}
                        # chosen mapping using typical attribute names
                        if from_t == 'Person':
                            entry['person'] = f.get('name')
                        elif from_t == 'Company':
                            entry['company'] = f.get('name')
                        elif from_t == 'Team':
                            entry['team'] = f.get('name')
                        elif from_t == 'Product':
                            entry['product'] = f.get('name')
                        elif from_t == 'Project':
                            entry['project'] = f.get('name')
                        elif from_t == 'Client':
                            entry['client'] = f.get('name')
                        else:
                            entry[from_t.lower()] = f.get('name')

                        if to_t == 'Department':
                            entry['department'] = t.get('name')
                        elif to_t == 'Company':
                            entry['company'] = t.get('name')
                        elif to_t == 'Technology':
                            entry['technology'] = t.get('name')
                        elif to_t == 'Product':
                            entry['product'] = t.get('name')
                        elif to_t == 'Person':
                            entry['person'] = t.get('name')
                        else:
                            entry[to_t.lower()] = t.get('name')
                        rel_res[rel['name']].append(entry)
    # dedupe
    for k, v in rel_res.items():
        seen = set()
        uniq = []
        for it in v:
            key = tuple(sorted(it.items()))
            if key in seen:
                continue
            seen.add(key)
            uniq.append(it)
        rel_res[k] = uniq
    return rel_res
