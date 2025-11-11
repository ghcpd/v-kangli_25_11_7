"""
Relation Extraction Module for KGEB
Extracts relationships between entities from semi-structured enterprise text.
"""

import re
import json
from typing import Dict, List, Any, Optional
from entity_extraction import EntityExtractor


class RelationExtractor:
    """Extracts relations between entities from enterprise text documents."""
    
    def __init__(self, relations_schema: Dict[str, Dict], entities: Dict[str, List[Dict]]):
        """
        Initialize the relation extractor.
        
        Args:
            relations_schema: Dictionary mapping relation types to their definitions
            entities: Dictionary of extracted entities by type
        """
        self.relations_schema = relations_schema
        self.entities = entities
        self.extracted_relations = {rel_type: [] for rel_type in relations_schema.keys()}
        
        # Create lookup indices for fast entity matching
        self._build_indices()
    
    def _build_indices(self):
        """Build lookup indices for entities."""
        self.person_index = {p["name"]: p for p in self.entities.get("Person", [])}
        self.company_index = {c["name"]: c for c in self.entities.get("Company", [])}
        self.project_index = {p["name"]: p for p in self.entities.get("Project", [])}
        self.department_index = {d["name"]: d for d in self.entities.get("Department", [])}
        self.position_index = {p["title"]: p for p in self.entities.get("Position", [])}
    
    def extract_belongs_to(self, text: str) -> List[Dict[str, str]]:
        """Extract BelongsTo relations (Person -> Department)."""
        relations = []
        for person in self.entities.get("Person", []):
            person_name = person.get("name")
            department_name = person.get("department")
            if person_name and department_name:
                relations.append({
                    "person": person_name,
                    "department": department_name
                })
        return relations
    
    def extract_works_at(self, text: str) -> List[Dict[str, str]]:
        """Extract WorksAt relations (Person -> Company)."""
        relations = []
        # Pattern: "Name, age X, works at Company as Position"
        pattern = r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),\s+age\s+\d+,\s+works\s+at\s+([A-Za-z0-9\s]+?)\s+as'
        
        matches = re.finditer(pattern, text, re.MULTILINE)
        for match in matches:
            person_name = match.group(1).strip()
            company_name = match.group(2).strip()
            
            if person_name in self.person_index and company_name in self.company_index:
                relations.append({
                    "person": person_name,
                    "company": company_name
                })
        
        return relations
    
    def extract_manages_project(self, text: str) -> List[Dict[str, str]]:
        """Extract ManagesProject relations."""
        return self._extract_project_management_relation(text, "manages")
    
    def extract_leads_project(self, text: str) -> List[Dict[str, str]]:
        """Extract LeadsProject relations."""
        return self._extract_project_management_relation(text, "leads")
    
    def extract_oversees_project(self, text: str) -> List[Dict[str, str]]:
        """Extract OverseesProject relations."""
        return self._extract_project_management_relation(text, "oversees")
    
    def extract_supervises_project(self, text: str) -> List[Dict[str, str]]:
        """Extract SupervisesProject relations."""
        return self._extract_project_management_relation(text, "supervises")
    
    def extract_handles_project(self, text: str) -> List[Dict[str, str]]:
        """Extract HandlesProject relations."""
        return self._extract_project_management_relation(text, "handles")
    
    def extract_coordinates_project(self, text: str) -> List[Dict[str, str]]:
        """Extract CoordinatesProject relations."""
        return self._extract_project_management_relation(text, "coordinates")
    
    def extract_directs_project(self, text: str) -> List[Dict[str, str]]:
        """Extract DirectsProject relations."""
        return self._extract_project_management_relation(text, "directs")
    
    def _extract_project_management_relation(self, text: str, verb: str) -> List[Dict[str, str]]:
        """Generic function to extract project management relations."""
        relations = []
        # Pattern: "Name verb N projects: Project1, Project2, ..."
        pattern = rf'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+{verb}\s+\d+\s+projects?:\s+([A-Za-z0-9\-\s,]+)'
        
        matches = re.finditer(pattern, text, re.MULTILINE | re.IGNORECASE)
        for match in matches:
            person_name = match.group(1).strip()
            projects_str = match.group(2).strip()
            
            # Split projects by comma
            project_names = [p.strip() for p in projects_str.split(',')]
            
            for project_name in project_names:
                if person_name in self.person_index and project_name in self.project_index:
                    relations.append({
                        "person": person_name,
                        "project": project_name
                    })
        
        return relations
    
    def extract_owns_project(self, text: str) -> List[Dict[str, str]]:
        """Extract OwnsProject relations (Company -> Project)."""
        # Infer from person's company and their projects
        relations = []
        works_at_relations = self.extract_works_at(text)
        
        # Create person -> company mapping
        person_to_company = {rel["person"]: rel["company"] for rel in works_at_relations}
        
        # Get all project management relations
        all_project_relations = []
        all_project_relations.extend(self.extract_manages_project(text))
        all_project_relations.extend(self.extract_leads_project(text))
        all_project_relations.extend(self.extract_oversees_project(text))
        all_project_relations.extend(self.extract_supervises_project(text))
        all_project_relations.extend(self.extract_handles_project(text))
        all_project_relations.extend(self.extract_coordinates_project(text))
        all_project_relations.extend(self.extract_directs_project(text))
        
        # Map person -> project -> company
        seen = set()
        for rel in all_project_relations:
            person = rel.get("person")
            project = rel.get("project")
            company = person_to_company.get(person)
            
            if company and project:
                key = (company, project)
                if key not in seen:
                    seen.add(key)
                    relations.append({
                        "company": company,
                        "project": project
                    })
        
        return relations
    
    def extract_has_position(self, text: str) -> List[Dict[str, str]]:
        """Extract HasPosition relations (Person -> Position)."""
        relations = []
        for person in self.entities.get("Person", []):
            person_name = person.get("name")
            position_title = person.get("position")
            if person_name and position_title:
                relations.append({
                    "person": person_name,
                    "position": position_title
                })
        return relations
    
    def extract_manages_department(self, text: str) -> List[Dict[str, str]]:
        """Extract ManagesDepartment relations."""
        relations = []
        for department in self.entities.get("Department", []):
            dept_name = department.get("name")
            head = department.get("head")
            if dept_name and head:
                relations.append({
                    "person": head,
                    "department": dept_name
                })
        return relations
    
    def extract_located_in(self, text: str) -> List[Dict[str, str]]:
        """Extract LocatedIn relations (Company -> Location)."""
        relations = []
        for company in self.entities.get("Company", []):
            company_name = company.get("name")
            location_city = company.get("location")
            if company_name and location_city:
                relations.append({
                    "company": company_name,
                    "location": location_city
                })
        return relations
    
    def extract_all(self, text: str) -> Dict[str, List[Dict[str, str]]]:
        """Extract all relation types from text."""
        relations = {}
        
        # Extract all defined relation types
        relations["BelongsTo"] = self.extract_belongs_to(text)
        relations["WorksAt"] = self.extract_works_at(text)
        relations["ManagesProject"] = self.extract_manages_project(text)
        relations["LeadsProject"] = self.extract_leads_project(text)
        relations["OverseesProject"] = self.extract_oversees_project(text)
        relations["SupervisesProject"] = self.extract_supervises_project(text)
        relations["HandlesProject"] = self.extract_handles_project(text)
        relations["CoordinatesProject"] = self.extract_coordinates_project(text)
        relations["DirectsProject"] = self.extract_directs_project(text)
        relations["OwnsProject"] = self.extract_owns_project(text)
        relations["HasPosition"] = self.extract_has_position(text)
        relations["ManagesDepartment"] = self.extract_manages_department(text)
        relations["LocatedIn"] = self.extract_located_in(text)
        
        # Initialize empty lists for relations not found in current dataset
        for rel_type in self.relations_schema.keys():
            if rel_type not in relations:
                relations[rel_type] = []
        
        return relations


def extract_relations(documents_path: str, relations_schema_path: str, 
                     entities_path: str, output_path: str):
    """
    Main function to extract relations from documents.
    
    Args:
        documents_path: Path to documents.txt
        relations_schema_path: Path to relations.json
        entities_path: Path to entities_output.json
        output_path: Path to save relations_output.json
    """
    # Load relations schema
    with open(relations_schema_path, 'r', encoding='utf-8') as f:
        relations_schema = json.load(f)
    
    # Load entities
    with open(entities_path, 'r', encoding='utf-8') as f:
        entities = json.load(f)
    
    # Load documents
    with open(documents_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Extract relations
    extractor = RelationExtractor(relations_schema, entities)
    relations = extractor.extract_all(text)
    
    # Save output
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(relations, f, indent=2, ensure_ascii=False)
    
    print(f"Extracted relations saved to {output_path}")
    return relations


if __name__ == "__main__":
    extract_relations("documents.txt", "relations.json", "entities_output.json", "relations_output.json")

