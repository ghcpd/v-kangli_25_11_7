import re
from datetime import datetime
from typing import List, Dict

# Lightweight heuristics for entity extraction. Not exhaustive; intended for benchmarking

NAME_RE = re.compile(r"\b[A-Z][a-z]+(?: [A-Z][a-z]+)+\b")
DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")
AGE_RE = re.compile(r"\bage[: ]?(\d{1,2})\b|\b(\d{1,2}) years old\b|\b(\d{1,2})yo\b", re.I)
MONEY_RE = re.compile(r"\$\s?([0-9,]+(?:\.[0-9]{2})?)|([0-9,]+) USD|¥\s?([0-9,]+)")
COMPANY_RE = re.compile(r"\b[A-Z][A-Za-z0-9&]+ (?:Inc\.|Inc|LLC|Ltd\.|Ltd|Corp\.|Corp|Co\.|Co)\b")
INDUSTRY_RE = re.compile(r"industry[: ]([A-Za-z &/]+)", re.I)
LOCATION_RE = re.compile(r"(Shanghai|Beijing|Shenzhen|Hangzhou|New York|San Francisco|London|Hong Kong)\b")
POSITION_RE = re.compile(r"position[: ]([A-Za-z0-9 &/-]+)|works as ([A-Za-z0-9 &/-]+)", re.I)


def _first_or_none(match):
    if not match:
        return None
    for g in match.groups():
        if g:
            return g.strip()
    return None


def extract_entities_from_text(text: str, schema: Dict[str, List[str]]):
    result = {ent: [] for ent in schema}

    # Find candidates for names and companies across the text
    names = NAME_RE.findall(text)
    companies = COMPANY_RE.findall(text)
    dates = DATE_RE.findall(text)
    ages = AGE_RE.findall(text)

    # Helper: gather by types
    # Person
    person_names = []
    for n in names:
        # Heuristic: skip company-like "Something Inc" matches
        if any(suffix in n for suffix in ['Inc', 'Ltd', 'LLC', 'Corp', 'Co']):
            continue
        person_names.append(n)

    for n in person_names:
        ent = {attr: None for attr in schema['Person']}
        ent['name'] = n
        # try to find age mention near the name
        match = re.search(rf"{re.escape(n)}[\s\S]{{0,60}}?((?:age[: ]?\d{{1,2}}|\d{{1,2}} years old))", text, re.I)
        if match:
            age_match = AGE_RE.search(match.group(1))
            age = _first_or_none(age_match)
            try:
                ent['age'] = int(age) if age else None
            except Exception:
                ent['age'] = None
        else:
            ent['age'] = None
        # position and department heuristics
        pos = POSITION_RE.search(text)
        ent['position'] = _first_or_none(pos.groups()) if pos else None
        dept = re.search(r"department[: ]([A-Za-z &/-]+)", text, re.I)
        ent['department'] = dept.group(1).strip() if dept else None
        result['Person'].append(ent)

    # Company
    for co in companies:
        ent = {attr: None for attr in schema['Company']}
        ent['name'] = co
        ind = INDUSTRY_RE.search(text)
        ent['industry'] = ind.group(1).strip() if ind else None
        loc = LOCATION_RE.search(text)
        ent['location'] = loc.group(1) if loc else None
        # sector guess from industry
        ent['sector'] = ent['industry'] if ent['industry'] else None
        result['Company'].append(ent)

    # Project
    for m in re.finditer(r"project[: ]([A-Za-z0-9 &-]+)", text, re.I):
        name = m.group(1)
        ent = {attr: None for attr in schema['Project']}
        ent['name'] = name.strip()
        # dates and status
        ent['start_date'] = DATE_RE.search(text).group(1) if DATE_RE.search(text) else None
        ent['end_date'] = None  # optional
        if 'ongoing' in text.lower() or 'in progress' in text.lower():
            ent['status'] = 'Ongoing'
        else:
            ent['status'] = None
        budget_match = MONEY_RE.search(text)
        ent['budget'] = int(budget_match.group(1).replace(',', '')) if budget_match else None
        result['Project'].append(ent)

    # Department
    for m in re.finditer(r"department[: ]([A-Za-z &/-]+)", text, re.I):
        name = m.group(1).strip()
        ent = {attr: None for attr in schema['Department']}
        ent['name'] = name
        # head: person near the string
        p = re.search(rf"{re.escape(name)}[\s\S]{{0,60}}?([A-Z][a-z]+ [A-Z][a-z]+)", text)
        ent['head'] = p.group(1) if p else None
        # employee count
        count = re.search(rf"{re.escape(name)}[\s\S]{{0,60}}?(\d{{2,4}}) employees?", text, re.I)
        ent['employee_count'] = int(count.group(1)) if count else None
        result['Department'].append(ent)

    # Technology
    for m in re.finditer(r"technology[: ]([A-Za-z0-9 &/-]+)|uses ([A-Za-z0-9 &/-]+) technology", text, re.I):
        name = m.group(1) or m.group(2)
        ent = {attr: None for attr in schema['Technology']}
        ent['name'] = name
        ent['category'] = None
        v = re.search(r"v(?:ersion)?[: ]?([0-9.]+)", text, re.I)
        ent['version'] = v.group(1) if v else None
        result['Technology'].append(ent)

    # Team
    for m in re.finditer(r"team[: ]([A-Za-z0-9 &/-]+)", text, re.I):
        name = m.group(1)
        ent = {attr: None for attr in schema['Team']}
        ent['name'] = name.strip()
        size = re.search(rf"{re.escape(name)}[\s\S]{{0,60}}?(\d{{1,3}}) members|size[: ](\d{{1,3}})", text, re.I)
        ent['size'] = int(_first_or_none(size.groups())) if size else None
        ent['focus_area'] = None
        result['Team'].append(ent)

    # Product
    for m in re.finditer(r"product[: ]([A-Za-z0-9 &/-]+)", text, re.I):
        name = m.group(1)
        ent = {attr: None for attr in schema['Product']}
        ent['name'] = name
        ent['version'] = None
        rel = DATE_RE.search(text)
        ent['release_date'] = rel.group(1) if rel else None
        result['Product'].append(ent)

    # Client
    for m in re.finditer(r"client[: ]([A-Za-z0-9 &/-]+)", text, re.I):
        name = m.group(1)
        ent = {attr: None for attr in schema['Client']}
        ent['name'] = name
        money = MONEY_RE.search(text)
        ent['contract_value'] = int(money.group(1).replace(',', '')) if money else None
        ent['industry'] = None
        result['Client'].append(ent)

    # Location
    for m in LOCATION_RE.finditer(text):
        ent = {attr: None for attr in schema['Location']}
        ent['city'] = m.group(1)
        ent['country'] = None
        ent['office_type'] = None
        result['Location'].append(ent)

    # Position
    for m in POSITION_RE.finditer(text):
        title = m.group(1) or m.group(2)
        ent = {attr: None for attr in schema['Position']}
        ent['title'] = title
        ent['level'] = None
        ent['salary_range'] = None
        result['Position'].append(ent)

    # Deduplicate lists (very naive)
    for k, items in result.items():
        seen = set()
        uniq = []
        for it in items:
            key = tuple(sorted((str(v) for v in it.values())))
            if key in seen:
                continue
            seen.add(key)
            uniq.append(it)
        result[k] = uniq
    return result
