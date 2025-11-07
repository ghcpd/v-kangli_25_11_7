import re
from typing import List, Dict, Any

ENTITY_SCHEMA = {
    "Person": ["name", "age", "position", "department"],
    "Company": ["name", "industry", "sector", "location"],
    "Project": ["name", "start_date", "end_date", "status", "budget"],
    "Department": ["name", "head", "employee_count"],
    "Position": ["title", "level", "salary_range"],
    "Technology": ["name", "category", "version"],
    "Location": ["city", "country", "office_type"],
    "Team": ["name", "size", "focus_area"],
    "Product": ["name", "version", "release_date"],
    "Client": ["name", "contract_value", "industry"],
}

NAME_RE = re.compile(r"([A-Z][a-z]+\s[A-Z][a-z]+)")
YEAR_RE = re.compile(r"(20\d{2})")
MONEY_RE = re.compile(r"\$?([0-9,]+)\s*(USD|usd|CNY|¥)?")

def extract_entities(doc: str) -> Dict[str, List[Dict[str, Any]]]:
    # very simple heuristics-based extractor to populate schema fields when possible
    out = {k: [] for k in ENTITY_SCHEMA}

    # find all name-like tokens
    names = set(NAME_RE.findall(doc))

    # Persons: look for 'age', 'position', 'department'
    for name in names:
        person = {"name": name}
        m_age = re.search(rf"{re.escape(name)}.*?age\s*(?:is|:)\s*(\d{{1,3}})", doc, re.IGNORECASE | re.S)
        if m_age:
            person["age"] = int(m_age.group(1))
        m_pos = re.search(rf"{re.escape(name)}.*?(?:position|title)\s*(?:is|:)\s*([A-Za-z0-9\s/\-]+)", doc, re.IGNORECASE | re.S)
        if m_pos:
            person["position"] = m_pos.group(1).strip()
        m_dep = re.search(rf"{re.escape(name)}.*?(?:department)\s*(?:is|:)\s*([A-Za-z&\-\s]+)", doc, re.IGNORECASE | re.S)
        if m_dep:
            person["department"] = m_dep.group(1).strip()
        if len(person) > 1:
            out["Person"].append(person)

    # Companies: look for 'Inc', 'Ltd', 'Corporation' or company keywords
    for comp in re.findall(r"([A-Z][a-zA-Z0-9& ]+(?:Inc|Ltd|LLC|Corporation|Group|Co\.|Company))", doc):
        c = {"name": comp.strip()}
        m_loc = re.search(rf"{re.escape(comp)}.*?(?:located in|location|headquartered in)\s*([A-Za-z,\s]+)", doc, re.IGNORECASE | re.S)
        if m_loc:
            c["location"] = m_loc.group(1).strip()
        out["Company"].append(c)

    # Projects: look for 'Project: <name>' or 'Project <name>' and dates/budget
    for m in re.finditer(r"Project[:\s]+([A-Za-z0-9 &-]+)", doc):
        name = m.group(1).strip()
        p = {"name": name}
        m_dates = re.search(rf"{re.escape(name)}.*?(\d{{4}}-\d{{2}}-\d{{2}}).*?(\d{{4}}-\d{{2}}-\d{{2}})", doc, re.IGNORECASE | re.S)
        if m_dates:
            p["start_date"] = m_dates.group(1)
            p["end_date"] = m_dates.group(2)
        m_budget = MONEY_RE.search(doc)
        if m_budget:
            p["budget"] = int(m_budget.group(1).replace(",", ""))
        out["Project"].append(p)

    # Departments, Teams, Products - simple name captures
    for dept in re.findall(r"Department[:\s]+([A-Za-z &-]+)", doc):
        out["Department"].append({"name": dept.strip()})

    for team in re.findall(r"Team[:\s]+([A-Za-z &-]+)", doc):
        out["Team"].append({"name": team.strip()})

    for prod in re.findall(r"Product[:\s]+([A-Za-z0-9 &-]+)", doc):
        out["Product"].append({"name": prod.strip()})

    return out
