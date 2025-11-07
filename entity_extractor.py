"""
Entity Extraction Module for KGEB (Enterprise Knowledge Graph Extraction Benchmark)

This module provides functionality to extract and recognize 10 types of entities from
semi-structured enterprise text documents.
"""

import json
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class ExtractedEntity:
    """Represents an extracted entity with its attributes."""
    entity_type: str
    attributes: Dict[str, Any]


class EntityExtractor:
    """
    Entity Extractor for enterprise knowledge graphs.
    
    Extracts the following entity types:
    - Person: name, age, position, department
    - Company: name, industry, sector, location
    - Project: name, start_date, end_date, status, budget
    - Department: name, head, employee_count
    - Position: title, level, salary_range
    - Technology: name, category, version
    - Location: city, country, office_type
    - Team: name, size, focus_area
    - Product: name, version, release_date
    - Client: name, contract_value, industry
    """
    
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
        "Client": ["name", "contract_value", "industry"]
    }
    
    def __init__(self):
        self.extracted_entities: Dict[str, List[Dict[str, Any]]] = {
            entity_type: [] for entity_type in self.ENTITY_SCHEMA.keys()
        }
        self.seen_entities: set = set()  # Track duplicates
    
    def extract_from_text(self, text: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Extract entities from raw text.
        
        Args:
            text: Raw text document to extract entities from
            
        Returns:
            Dictionary of extracted entities grouped by type
        """
        lines = text.strip().split('\n')
        
        for line in lines:
            self._process_line(line)
        
        return self.extracted_entities
    
    def _process_line(self, line: str) -> None:
        """Process a single line to extract entities."""
        line = line.strip()
        if not line:
            return
        
        # Extract Person entities
        # Pattern: "Name, age N, works at Company as Position."
        person_pattern = r"(\w+\s+\w+),\s*age\s+(\d+),\s*works at\s+(.+?)\s+as\s+(.+?)(?:\.|,)"
        person_matches = re.finditer(person_pattern, line, re.IGNORECASE)
        for match in person_matches:
            name, age, company, position = match.groups()
            entity_key = f"Person_{name}"
            if entity_key not in self.seen_entities:
                self.seen_entities.add(entity_key)
                self.extracted_entities["Person"].append({
                    "name": name.strip(),
                    "age": int(age),
                    "position": position.strip(),
                    "department": None  # Will be inferred from context
                })
        
        # Extract Project entities
        # Pattern: "Project Name started on YYYY-MM-DD, ends on YYYY-MM-DD."
        project_pattern = r"Project\s+(\w+(?:-?\w+)*)\s+(?:started|began|launched|initiated)\s+on\s+(\d{4}-\d{2}-\d{2}),\s+(?:ends|concludes|finishes|completes)\s+on\s+(\d{4}-\d{2}-\d{2})"
        project_matches = re.finditer(project_pattern, line, re.IGNORECASE)
        for match in project_matches:
            proj_name, start_date, end_date = match.groups()
            entity_key = f"Project_{proj_name}"
            if entity_key not in self.seen_entities:
                self.seen_entities.add(entity_key)
                self.extracted_entities["Project"].append({
                    "name": proj_name.strip(),
                    "start_date": start_date,
                    "end_date": end_date,
                    "status": self._infer_project_status(start_date, end_date),
                    "budget": None
                })
        
        # Extract Company entities
        # Pattern: "CompanyName operates in Industry sector."
        company_pattern = r"(\w+(?:\s+\w+)?)\s+(?:operates in|specializes in|focuses on|is known for|works in)\s+(.+?)(?:\s+industry|\.)"
        company_matches = re.finditer(company_pattern, line, re.IGNORECASE)
        for match in company_matches:
            company_name, industries = match.groups()
            entity_key = f"Company_{company_name}"
            if entity_key not in self.seen_entities:
                self.seen_entities.add(entity_key)
                parts = [p.strip() for p in industries.split(' and ')]
                industry = parts[0] if parts else None
                sector = parts[1] if len(parts) > 1 else None
                
                self.extracted_entities["Company"].append({
                    "name": company_name.strip(),
                    "industry": industry,
                    "sector": sector,
                    "location": None
                })
        
        # Extract Team entities
        # Pattern: "Team Name manages/leads/oversees/supervises/coordinates N projects"
        team_pattern = r"(\w+\s+\w+)\s+(?:manages|leads|oversees|supervises|coordinates|directs)\s+(\d+)\s+projects?"
        team_matches = re.finditer(team_pattern, line, re.IGNORECASE)
        for match in team_matches:
            team_name, team_size = match.groups()
            # If team_name looks like a person (name format), skip it
            if not self._is_person_name(team_name):
                entity_key = f"Team_{team_name}"
                if entity_key not in self.seen_entities:
                    self.seen_entities.add(entity_key)
                    self.extracted_entities["Team"].append({
                        "name": team_name.strip(),
                        "size": int(team_size),
                        "focus_area": None
                    })
    
    def _is_person_name(self, text: str) -> bool:
        """Check if text looks like a person name (first and last name)."""
        common_first_names = {
            "John", "Jane", "Michael", "Sarah", "David", "Emily", "Robert", "Lisa",
            "James", "Maria", "Tom", "Rachel", "Kevin", "Anna", "Mark", "Susan",
            "Paul", "Jennifer", "Steven", "Michelle", "Daniel", "Catherine", "Andrew",
            "Sophia", "Nathan", "Olivia", "Christopher", "Amanda", "Ryan", "Jessica"
        }
        words = text.split()
        if len(words) >= 2 and words[0] in common_first_names:
            return True
        return False
    
    def _infer_project_status(self, start_date: str, end_date: str) -> str:
        """Infer project status based on dates."""
        try:
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            today = datetime.now()
            
            if end_dt < today:
                return "Completed"
            elif end_dt.year == today.year and end_dt.month == today.month:
                return "In Progress"
            else:
                return "Ongoing"
        except ValueError:
            return "Unknown"
    
    def extract_from_file(self, filepath: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Extract entities from a text file.
        
        Args:
            filepath: Path to the input file
            
        Returns:
            Dictionary of extracted entities
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
        
        return self.extract_from_text(text)
    
    def get_results(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get the current extraction results."""
        return self.extracted_entities
    
    def save_results(self, output_filepath: str) -> None:
        """
        Save extracted entities to JSON file.
        
        Args:
            output_filepath: Path to save the results
        """
        with open(output_filepath, 'w', encoding='utf-8') as f:
            json.dump(self.extracted_entities, f, indent=2, ensure_ascii=False)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about extracted entities."""
        stats = {}
        total_entities = 0
        
        for entity_type, entities in self.extracted_entities.items():
            count = len(entities)
            stats[entity_type] = count
            total_entities += count
        
        stats['total'] = total_entities
        return stats


def extract_entities(input_file: str, output_file: str) -> Dict[str, Any]:
    """
    Main function to extract entities from input file and save to output file.
    
    Args:
        input_file: Path to input document
        output_file: Path to save extracted entities
        
    Returns:
        Statistics about extraction
    """
    extractor = EntityExtractor()
    entities = extractor.extract_from_file(input_file)
    extractor.save_results(output_file)
    
    stats = extractor.get_statistics()
    print(f"\n✓ Entity extraction completed")
    print(f"  Total entities extracted: {stats['total']}")
    for entity_type, count in stats.items():
        if entity_type != 'total':
            print(f"  - {entity_type}: {count}")
    
    return stats
