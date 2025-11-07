"""
Simple rule-based entity and relation extractor for KGEB baseline.
"""
import re
import json
from typing import List, Dict, Any
from pathlib import Path


def parse_documents(doc_path: str) -> List[str]:
    with open(doc_path, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]
    return lines


def parse_documents_dir(dir_path: str) -> List[str]:
    from pathlib import Path
    lines = []
    p = Path(dir_path)
    for f in p.glob('*.txt'):
        with open(f, 'r', encoding='utf-8') as fh:
            for l in fh:
                l = l.strip()
                if l:
                    lines.append(l)
    return lines


def extract_persons(lines: List[str]) -> List[Dict[str, Any]]:
    persons = []
    for line in lines:
        # match lines like "John Doe, age 32, works at OpenAI as a Researcher."
        m = re.match(r"([A-Z][a-z]+(?: [A-Z][a-z]+)+), age (\d+), works at ([A-Za-z0-9 &]+)(?: as a ([A-Za-z ]+))?\.", line)
        if m:
            name = m.group(1).strip()
            age = int(m.group(2))
            company = m.group(3).strip()
            position = (m.group(4) or "").strip()
            persons.append({"name": name, "age": age, "position": position, "department": ""})
    return persons


def extract_companies(lines: List[str]) -> List[Dict[str, Any]]:
    companies = {}
    # e.g., "OpenAI operates in the Technology industry."
    for line in lines:
        m = re.match(r"([A-Z][A-Za-z0-9 &]+) operates in the (.+?) industry\.", line)
        if m:
            name = m.group(1).strip()
            industry = m.group(2).strip()
            companies[name] = {"name": name, "industry": industry, "sector": "", "location": ""}
        # "Google specializes in Technology and Internet Services."
        m2 = re.match(r"([A-Z][A-Za-z0-9 &]+) specializes in (.+?)\.", line)
        if m2:
            name = m2.group(1).strip()
            industry = m2.group(2).strip()
            if name not in companies:
                companies[name] = {"name": name, "industry": industry, "sector": "", "location": ""}
            else:
                companies[name]["industry"] = industry
    return list(companies.values())


def extract_projects(lines: List[str]) -> List[Dict[str, Any]]:
    projects = {}
    for line in lines:
        # Project Alpha started on 2023-01-15, ends on 2023-06-30.
        m = re.match(r"Project ([A-Za-z0-9\-]+) (?:started|began|launched|initiated|started) on (\d{4}-\d{2}-\d{2}), (?:ends|ends on|concludes|concludes on|finishes|finishes on|completes|completes on) (\d{4}-\d{2}-\d{2})\.", line)
        if m:
            name = m.group(1).strip()
            start = m.group(2)
            end = m.group(3)
            projects[name] = {"name": name, "start_date": start, "end_date": end, "status": "", "budget": None}
    return list(projects.values())


def extract_relations(lines: List[str]) -> List[Dict[str, Any]]:
    relations = []
    # works at -> employee of
    for line in lines:
        m = re.match(r"([A-Z][a-z]+(?: [A-Z][a-z]+)+), age (\d+), works at ([A-Za-z0-9 &]+)(?: as a ([A-Za-z ]+))?\.", line)
        if m:
            relations.append({"type": "EmployeeOf", "person": m.group(1).strip(), "company": m.group(3).strip()})
    # manages N projects: list
    for line in lines:
        m = re.match(r"([A-Z][a-z]+(?: [A-Z][a-z]+)+) (?:manages|leads|oversees|supervises|handles|coordinates|directs|manages) (?:\d+ )?projects?: (.+)\.", line)
        if m:
            name = m.group(1).strip()
            projects = [p.strip() for p in re.split(r",|;", m.group(2))]
            for p in projects:
                # strip trailing numbers or 'projects:' words
                relations.append({"type": "ManagesProject", "person": name, "project": p})
    # Company operates in industry -> CompanyInIndustry
    for line in lines:
        m = re.match(r"([A-Z][A-Za-z0-9 &]+) operates in the (.+?) industry\.", line)
        if m:
            relations.append({"type": "CompanyInIndustry", "company": m.group(1).strip(), "industry": m.group(2).strip()})
    return relations


def extract_all(lines: List[str]) -> Dict[str, Any]:
    persons = extract_persons(lines)
    companies = extract_companies(lines)
    projects = extract_projects(lines)
    relations = extract_relations(lines)
    entities = {
        "Person": persons,
        "Company": companies,
        "Project": projects
    }
    relations_grouped = {}
    for rel in relations:
        relations_grouped.setdefault(rel["type"], []).append({k: v for k, v in rel.items() if k != "type"})
    return {"entities": entities, "relations": relations_grouped}


def save_json(data: Any, path: str):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    # write atomically to avoid partial writes during concurrent access
    import os, tempfile
    dirpath = Path(path).parent
    fd, tmp = tempfile.mkstemp(dir=dirpath)
    with os.fdopen(fd, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)


if __name__ == "__main__":
    import sys
    doc_path = sys.argv[1] if len(sys.argv) > 1 else "documents.txt"
    lines = parse_documents(doc_path)
    out = extract_all(lines)
    save_json(out["entities"], "entities_output.json")
    save_json(out["relations"], "relations_output.json")
    print("Extracted entities and relations to entities_output.json and relations_output.json")
