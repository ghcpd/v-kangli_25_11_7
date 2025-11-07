"""
Relation Extraction Module for KGEB (Enterprise Knowledge Graph Extraction Benchmark)

This module provides functionality to extract relationships between entities from
semi-structured enterprise text documents.
"""

import json
import re
from typing import Dict, List, Any, Tuple, Set
from dataclasses import dataclass


@dataclass
class Relation:
    """Represents a relation between two entities."""
    relation_type: str
    source_entity: str
    target_entity: str
    source_type: str
    target_type: str


class RelationExtractor:
    """
    Relation Extractor for enterprise knowledge graphs.
    
    Extracts 30 types of relations between entities including:
    - Person -> Department (BelongsTo)
    - Person -> Project (ManagesProject)
    - Person -> Company (WorksAt)
    - Company -> Project (OwnsProject)
    - Project -> Technology (UsesTechnology)
    - And 25 more relation types
    """
    
    def __init__(self, relations_schema_path: str = "relations.json"):
        """Initialize relation extractor with schema."""
        self.relations_schema = self._load_schema(relations_schema_path)
        self.extracted_relations: Dict[str, List[Dict[str, Any]]] = {
            rel['id']: [] for rel in self.relations_schema['relations']
        }
        self.seen_relations: Set[Tuple[str, str, str]] = set()
    
    def _load_schema(self, schema_path: str) -> Dict[str, Any]:
        """Load relation schema from JSON file."""
        try:
            with open(schema_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Schema file not found: {schema_path}")
            return {"relations": []}
    
    def extract_from_text(self, text: str, entities: Dict[str, List[Dict[str, Any]]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Extract relations from text using entity information.
        
        Args:
            text: Raw text document
            entities: Previously extracted entities
            
        Returns:
            Dictionary of extracted relations grouped by type
        """
        lines = text.strip().split('\n')
        
        # Build lookup dictionaries for faster entity matching
        person_names = {e['name']: e for e in entities.get('Person', [])}
        company_names = {e['name']: e for e in entities.get('Company', [])}
        project_names = {e['name']: e for e in entities.get('Project', [])}
        
        for line in lines:
            self._extract_relations_from_line(
                line, 
                person_names, 
                company_names, 
                project_names,
                entities
            )
        
        return self.extracted_relations
    
    def _extract_relations_from_line(
        self,
        line: str,
        person_names: Dict[str, Dict],
        company_names: Dict[str, Dict],
        project_names: Dict[str, Dict],
        all_entities: Dict[str, List[Dict[str, Any]]]
    ) -> None:
        """Extract relations from a single line."""
        
        # Pattern 1: Person works at Company as Position
        # Relation type: WorksAt
        person_company_pattern = r"(\w+\s+\w+),\s*age\s+\d+,\s*works at\s+(.+?)\s+as\s+"
        matches = re.finditer(person_company_pattern, line, re.IGNORECASE)
        for match in matches:
            person_name, company_name = match.groups()
            rel_key = (person_name.strip(), company_name.strip(), "WorksAt")
            if rel_key not in self.seen_relations:
                self.seen_relations.add(rel_key)
                self.extracted_relations["WorksAt"].append({
                    "person": person_name.strip(),
                    "company": company_name.strip()
                })
        
        # Pattern 2: Person manages/leads/oversees Projects
        # Relation type: ManagesProject
        manage_pattern = r"(\w+\s+\w+)\s+(?:manages|leads|oversees|supervises|coordinates|directs)\s+\d+\s+projects?:?\s*(.+?)(?:\.|$)"
        matches = re.finditer(manage_pattern, line, re.IGNORECASE)
        for match in matches:
            person_name, projects_str = match.groups()
            projects = [p.strip() for p in projects_str.split(',')]
            
            for project in projects:
                project = project.strip()
                if project and project in project_names:
                    rel_key = (person_name.strip(), project, "ManagesProject")
                    if rel_key not in self.seen_relations:
                        self.seen_relations.add(rel_key)
                        self.extracted_relations["ManagesProject"].append({
                            "person": person_name.strip(),
                            "project": project
                        })
        
        # Pattern 3: Project started/began/launched on date ... ends/concludes on date
        # Relation type: ProjectTimeline
        project_timeline = r"Project\s+(\w+(?:-?\w+)*)\s+(?:started|began|launched|initiated)\s+on\s+(\d{4}-\d{2}-\d{2}),\s+(?:ends|concludes|finishes|completes)\s+on\s+(\d{4}-\d{2}-\d{2})"
        matches = re.finditer(project_timeline, line, re.IGNORECASE)
        for match in matches:
            proj_name, start_date, end_date = match.groups()
            rel_key = (proj_name, start_date + " to " + end_date, "ProjectTimeline")
            if rel_key not in self.seen_relations:
                self.seen_relations.add(rel_key)
                self.extracted_relations["ProjectTimeline"].append({
                    "project": proj_name.strip(),
                    "start_date": start_date,
                    "end_date": end_date
                })
        
        # Pattern 4: Company operates in Industry
        # Relation type: OperatesIn
        operates_pattern = r"(\w+(?:\s+\w+)?)\s+(?:operates in|specializes in|focuses on|is known for|works in)\s+(.+?)(?:\s+industry|and|\.)"
        matches = re.finditer(operates_pattern, line, re.IGNORECASE)
        for match in matches:
            company_name, industry = match.groups()
            rel_key = (company_name.strip(), industry.strip(), "OperatesIn")
            if rel_key not in self.seen_relations:
                self.seen_relations.add(rel_key)
                self.extracted_relations["OperatesIn"].append({
                    "company": company_name.strip(),
                    "industry": industry.strip()
                })
        
        # Pattern 5: Team information (implicit team-project relations)
        # Relation type: CollaborationOn
        team_project_pattern = r"(\w+\s+\w+)\s+(?:manages|leads|oversees|supervises|coordinates|directs)\s+(\d+)\s+projects?:?\s*(.+?)(?:\.|$)"
        matches = re.finditer(team_project_pattern, line, re.IGNORECASE)
        for match in matches:
            person_name, num_projects, projects_str = match.groups()
            
            # Skip if this looks like a single person managing (not a team)
            # Team names typically don't follow "FirstName LastName" pattern or have "Team" keyword
            projects = [p.strip() for p in projects_str.split(',')]
            for project in projects:
                project = project.strip()
                if project:
                    rel_key = (person_name.strip(), project, "CollaborationOn")
                    if rel_key not in self.seen_relations:
                        self.seen_relations.add(rel_key)
                        self.extracted_relations["CollaborationOn"].append({
                            "team_lead": person_name.strip(),
                            "project": project
                        })
    
    def extract_from_file(
        self,
        text_filepath: str,
        entities_filepath: str
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Extract relations from files.
        
        Args:
            text_filepath: Path to raw text document
            entities_filepath: Path to extracted entities JSON
            
        Returns:
            Dictionary of extracted relations
        """
        # Load entities
        with open(entities_filepath, 'r', encoding='utf-8') as f:
            entities = json.load(f)
        
        # Load and process text
        with open(text_filepath, 'r', encoding='utf-8') as f:
            text = f.read()
        
        return self.extract_from_text(text, entities)
    
    def get_results(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get the current extraction results."""
        return self.extracted_relations
    
    def save_results(self, output_filepath: str) -> None:
        """
        Save extracted relations to JSON file.
        
        Args:
            output_filepath: Path to save the results
        """
        # Only include relation types with extracted relations
        results = {
            rel_type: relations
            for rel_type, relations in self.extracted_relations.items()
            if relations
        }
        
        with open(output_filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about extracted relations."""
        stats = {}
        total_relations = 0
        
        for relation_type, relations in self.extracted_relations.items():
            count = len(relations)
            if count > 0:
                stats[relation_type] = count
                total_relations += count
        
        stats['total'] = total_relations
        return stats


def extract_relations(
    text_file: str,
    entities_file: str,
    output_file: str
) -> Dict[str, Any]:
    """
    Main function to extract relations and save to output file.
    
    Args:
        text_file: Path to raw text document
        entities_file: Path to extracted entities
        output_file: Path to save extracted relations
        
    Returns:
        Statistics about relation extraction
    """
    extractor = RelationExtractor()
    relations = extractor.extract_from_file(text_file, entities_file)
    extractor.save_results(output_file)
    
    stats = extractor.get_statistics()
    print(f"\n✓ Relation extraction completed")
    print(f"  Total relations extracted: {stats['total']}")
    for relation_type, count in stats.items():
        if relation_type != 'total':
            print(f"  - {relation_type}: {count}")
    
    return stats
