import re
import json
from pathlib import Path
from typing import List, Dict, Any
from .config import load_entities_schema, load_relations_schema, load_documents

ROOT = Path(__file__).resolve().parent.parent

# Basic regex patterns for this corpus - simple baseline
PERSON_LINE_RE = re.compile(r"^(?P<name>[A-Za-z\-\s]+), age (?P<age>\d+), works at (?P<company>[A-Za-z\-]+) as a?n? ?(?P<position>[^.]+)\.")
PROJECT_LINE_RE = re.compile(r"Project (?P<name>[A-Za-z0-9\-]+) (?:started|began|launched|initiated) on (?P<start_date>\d{4}-\d{2}-\d{2}), (?:ends|ends on|concludes|concludes on|finishes|finishes on|completes|completes on) (?P<end_date>\d{4}-\d{2}-\d{2})\.")
MANAGES_LINE_RE = re.compile(r"^(?P<manager>[A-Za-z\-\s]+) manages (?P<count>\d+) projects: (?P<projects>[A-Za-z0-9\-,\s]+)\.")
LEADS_LINE_RE = re.compile(r"^(?P<manager>[A-Za-z\-\s]+) leads (?P<count>\d+) projects: (?P<projects>[A-Za-z0-9\-,\s]+)\.")
OVERSEES_LINE_RE = re.compile(r"^(?P<manager>[A-Za-z\-\s]+) oversees (?P<count>\d+) projects: (?P<projects>[A-Za-z0-9\-,\s]+)\.")
COMPANY_INDUSTRY_RE = re.compile(r"^(?P<company>[A-Za-z\-\s]+) (?:operates in|specializes in|focuses on|works in|is known for|is known for) the (?P<industry>[^.]+) industry(\.|\n)")
WORKS_AT_RE = re.compile(r"^(?P<name>[A-Za-z\-\s]+), age (?P<age>\d+), works at (?P<company>[A-Za-z\-\s]+) as a?n? ?(?P<position>[^.]+)\.")


def extract_entities(doc_lines: List[str], entities_schema: Dict[str, List[str]]) -> Dict[str, List[Dict[str, Any]]]:
    entities = {k: [] for k in entities_schema.keys()}

    companies_seen = {}

    for ln in doc_lines:
        ln = ln.strip()
        if not ln:
            continue

        # Person entries (name, age, works at COMPANY as POSITION.)
        m = WORKS_AT_RE.match(ln)
        if m:
            name = m.group("name").strip()
            age = int(m.group("age"))
            company = m.group("company").strip()
            position = m.group("position").strip()

            person = {"name": name, "age": age, "position": position, "department": None}
            entities["Person"].append(person)

            # add company entry if not present
            if company not in companies_seen:
                companies_seen[company] = {"name": company, "industry": None, "sector": None, "location": None}
                entities["Company"].append(companies_seen[company])
            continue

        # Project lines
        m = PROJECT_LINE_RE.match(ln)
        if m:
            name = m.group("name")
            start = m.group("start_date")
            end = m.group("end_date")
            project = {"name": name, "start_date": start, "end_date": end, "status": "Ongoing" if end >= "2023-11-07" else "Closed", "budget": None}
            entities["Project"].append(project)
            continue

        # Manages, leads, oversees.
        m = MANAGES_LINE_RE.match(ln) or LEADS_LINE_RE.match(ln) or OVERSEES_LINE_RE.match(ln)
        if m:
            manager = m.group("manager").strip()
            projects_list = [p.strip() for p in m.group("projects").split(",")]
            # Ensure manager exists in Person list
            if not any(p.get("name") == manager for p in entities["Person"]):
                entities["Person"].append({"name": manager, "age": None, "position": None, "department": None})
            for p in projects_list:
                # create project if not present
                if not any(pr.get("name") == p for pr in entities["Project"]):
                    entities["Project"].append({"name": p, "start_date": None, "end_date": None, "status": None, "budget": None})
            continue

        # Company industry lines
        m = COMPANY_INDUSTRY_RE.match(ln)
        if m:
            company = m.group("company").strip()
            industry = m.group("industry").strip()
            if company in companies_seen:
                companies_seen[company]["industry"] = industry
            else:
                companies_seen[company] = {"name": company, "industry": industry, "sector": None, "location": None}
                entities["Company"].append(companies_seen[company])
            continue

    # Deduplicate entries by name attribute for basic de-dup
    for etype, items in list(entities.items()):
        seen = {}
        unique = []
        for it in items:
            key = it.get("name") or json.dumps(it, sort_keys=True)
            if key in seen:
                # merge missing fields
                old = seen[key]
                for k, v in it.items():
                    if not old.get(k) and v:
                        old[k] = v
            else:
                seen[key] = it
                unique.append(it)
        entities[etype] = unique

    return entities


def extract_relations(doc_lines: List[str], entities_schema: Dict[str, List[str]], relations_schema: Dict[str, List[str]]) -> Dict[str, List[Dict[str, Any]]]:
    relations = {k: [] for k in relations_schema.keys()}

    # We will extract a few common relations: WorksAt, Manages, PersonWorkedOnProject, LocatedIn via simple linking
    # Parse again for People/company mapping and project managers
    person_company = {}
    person_projects = {}

    for ln in doc_lines:
        ln = ln.strip()
        m = WORKS_AT_RE.match(ln)
        if m:
            name = m.group("name").strip()
            company = m.group("company").strip()
            person_company[name] = company
            relations["WorksAt"].append({"person": name, "company": company})

        m = MANAGES_LINE_RE.match(ln) or LEADS_LINE_RE.match(ln) or OVERSEES_LINE_RE.match(ln)
        if m:
            manager = m.group("manager").strip()
            projects_list = [p.strip() for p in m.group("projects").split(",")]
            for p in projects_list:
                relations["Manages"].append({"person": manager, "project": p})
                # infer PersonWorkedOnProject
                relations["PersonWorkedOnProject"].append({"person": manager, "project": p})

    # infer owns projects where company's employee manages project -> company owns project
    for rel in relations["Manages"]:
        person = rel["person"]
        project = rel["project"]
        company = person_company.get(person)
        if company:
            relations["OwnsProject"].append({"company": company, "project": project})

    # infer LocatedIn from Company lines
    for ln in doc_lines:
        ln = ln.strip()
        # simple location detection: 'in [City]' or 'based in [City]'
        if "Shenzhen" in ln or "Hangzhou" in ln or "Shenzhen" in ln:
            # naive: find company and city
            words = ln.split()
            for c in ["Shenzhen", "Hangzhou"]:
                if c in ln:
                    # find company name (first word)
                    parts = ln.split()
                    company = parts[0]
                    relations.setdefault("LocatedIn", []).append({"company": company, "city": c})

    # deduplicate
    for rtype, items in list(relations.items()):
        unique = []
        seen = set()
        for it in items:
            key = json.dumps(it, sort_keys=True)
            if key not in seen:
                seen.add(key)
                unique.append(it)
        relations[rtype] = unique

    return relations


if __name__ == "__main__":
    docs = load_documents()
    schema = load_entities_schema()
    rels_schema = load_relations_schema()

    entities = extract_entities(docs, schema)
    relations = extract_relations(docs, schema, rels_schema)

    out_e = ROOT / "entities_output.json"
    out_r = ROOT / "relations_output.json"
    with open(out_e, "w", encoding="utf-8") as f:
        json.dump(entities, f, indent=2, ensure_ascii=False)
    with open(out_r, "w", encoding="utf-8") as f:
        json.dump(relations, f, indent=2, ensure_ascii=False)
    print(f"Wrote {out_e} and {out_r}")
