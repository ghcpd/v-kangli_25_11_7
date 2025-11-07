from typing import Dict, List, Any
import re

RELATION_SCHEMA = {
    "BelongsTo": ("Person", "Department"),
    "OwnsProject": ("Company", "Project"),
    "UsesTechnology": ("Team", "Technology"),
}

def extract_relations(doc: str, entities: Dict[str, List[Dict[str, Any]]]) -> Dict[str, List[Dict[str, Any]]]:
    out = {k: [] for k in RELATION_SCHEMA}

    # BelongsTo: look for patterns 'X is in Y' or 'X belongs to Y'
    for person in entities.get("Person", []):
        pname = person.get("name")
        if not pname:
            continue
        m = re.search(rf"{re.escape(pname)}.*?(?:belongs to|is in|works in|member of)\s+([A-Za-z &-]+)", doc, re.IGNORECASE)
        if m:
            out["BelongsTo"].append({"person": pname, "department": m.group(1).strip()})

    # OwnsProject: look for 'Company X ... project Y' patterns
    for comp in entities.get("Company", []):
        cname = comp.get("name")
        if not cname:
            continue
        for proj in entities.get("Project", []):
            pname = proj.get("name")
            if not pname:
                continue
            if re.search(rf"{re.escape(cname)}.*?(?:owns|launched|started|is executing).{0,40}{re.escape(pname)}", doc, re.IGNORECASE | re.S):
                out["OwnsProject"].append({"company": cname, "project": pname})

    # UsesTechnology: look for 'Team X uses Y' or 'uses technology Z'
    for team in entities.get("Team", []):
        tname = team.get("name")
        if not tname:
            continue
        m = re.search(rf"{re.escape(tname)}.*?(?:uses|utilizes|adopts)\s+([A-Za-z0-9 &-]+)", doc, re.IGNORECASE)
        if m:
            out["UsesTechnology"].append({"team": tname, "technology": m.group(1).strip()})

    return out
