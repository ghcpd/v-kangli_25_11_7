"""
Entity Extraction Module for KGEB
Extracts entities and their attributes from semi-structured enterprise text.
"""

import re
import json
from typing import Dict, List, Any
from datetime import datetime


class EntityExtractor:
    """Extracts entities from enterprise text documents."""
    
    def __init__(self, entities_schema: Dict[str, List[str]]):
        """
        Initialize the entity extractor.
        
        Args:
            entities_schema: Dictionary mapping entity types to their attributes
        """
        self.entities_schema = entities_schema
        self.extracted_entities = {entity_type: [] for entity_type in entities_schema.keys()}
        
    def extract_person(self, text: str) -> List[Dict[str, Any]]:
        """Extract Person entities from text."""
        persons = []
        # Pattern: "Name, age X, works at Company as Position"
        pattern = r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),\s+age\s+(\d+),\s+works\s+at\s+([A-Za-z0-9\s]+?)\s+as\s+(?:a\s+|an\s+)?([A-Za-z\s]+?)(?:\.|$)'
        
        matches = re.finditer(pattern, text, re.MULTILINE)
        for match in matches:
            name = match.group(1).strip()
            age = int(match.group(2))
            company = match.group(3).strip()
            position = match.group(4).strip()
            
            # Infer department from position or company context
            department = self._infer_department(position, company)
            
            persons.append({
                "name": name,
                "age": age,
                "position": position,
                "department": department
            })
        
        return persons
    
    def extract_company(self, text: str) -> List[Dict[str, Any]]:
        """Extract Company entities from text."""
        companies = []
        # Pattern: "Company operates/specializes/focuses/is known for/works in Industry and Sector"
        patterns = [
            r'([A-Za-z0-9]+)\s+operates\s+in\s+(?:the\s+)?([A-Za-z\s]+?)(?:\s+and\s+([A-Za-z\s]+?))?(?:industry|sector|\.|$)',
            r'([A-Za-z0-9]+)\s+specializes\s+in\s+([A-Za-z\s]+?)(?:\s+and\s+([A-Za-z\s]+?))?(?:industry|sector|\.|$)',
            r'([A-Za-z0-9]+)\s+focuses\s+on\s+([A-Za-z\s]+?)(?:\s+and\s+([A-Za-z\s]+?))?(?:industry|sector|\.|$)',
            r'([A-Za-z0-9]+)\s+is\s+known\s+for\s+([A-Za-z\s]+?)(?:\s+and\s+([A-Za-z\s]+?))?(?:industry|sector|\.|$)',
            r'([A-Za-z0-9]+)\s+works\s+in\s+([A-Za-z\s]+?)(?:\s+and\s+([A-Za-z\s]+?))?(?:sectors|industry|\.|$)'
        ]
        
        seen_companies = set()
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.MULTILINE | re.IGNORECASE)
            for match in matches:
                company_name = match.group(1).strip()
                if company_name in seen_companies:
                    continue
                seen_companies.add(company_name)
                
                industry = match.group(2).strip()
                sector = match.group(3).strip() if match.group(3) else industry
                
                # Infer location from company (simplified - in real scenario would use knowledge base)
                location = self._infer_location(company_name)
                
                companies.append({
                    "name": company_name,
                    "industry": industry,
                    "sector": sector,
                    "location": location
                })
        
        return companies
    
    def extract_project(self, text: str) -> List[Dict[str, Any]]:
        """Extract Project entities from text."""
        projects = []
        # Pattern: "Project Name started/began/launched/initiated on YYYY-MM-DD, ends/concludes/finishes/completes on YYYY-MM-DD"
        pattern = r'Project\s+([A-Za-z0-9\-]+)\s+(?:started|began|launched|initiated)\s+on\s+(\d{4}-\d{2}-\d{2}),\s+(?:ends|concludes|finishes|completes)\s+on\s+(\d{4}-\d{2}-\d{2})'
        
        matches = re.finditer(pattern, text, re.MULTILINE | re.IGNORECASE)
        for match in matches:
            project_name = match.group(1).strip()
            start_date = match.group(2).strip()
            end_date = match.group(3).strip()
            
            # Determine status based on dates
            status = self._determine_project_status(start_date, end_date)
            
            # Estimate budget (simplified - would use ML in production)
            budget = self._estimate_budget(project_name, start_date, end_date)
            
            projects.append({
                "name": project_name,
                "start_date": start_date,
                "end_date": end_date,
                "status": status,
                "budget": budget
            })
        
        return projects
    
    def extract_department(self, text: str, persons: List[Dict]) -> List[Dict[str, Any]]:
        """Extract Department entities from person data."""
        departments = {}
        
        for person in persons:
            dept_name = person.get("department", "Unknown")
            if dept_name not in departments:
                departments[dept_name] = {
                    "name": dept_name,
                    "head": None,  # Would need additional data
                    "employee_count": 0
                }
            departments[dept_name]["employee_count"] += 1
        
        return list(departments.values())
    
    def extract_position(self, text: str, persons: List[Dict]) -> List[Dict[str, Any]]:
        """Extract Position entities from person data."""
        positions = {}
        
        for person in persons:
            pos_title = person.get("position", "Unknown")
            if pos_title not in positions:
                positions[pos_title] = {
                    "title": pos_title,
                    "level": self._infer_level(pos_title),
                    "salary_range": self._estimate_salary_range(pos_title)
                }
        
        return list(positions.values())
    
    def extract_technology(self, text: str) -> List[Dict[str, Any]]:
        """Extract Technology entities from text."""
        # In this dataset, technologies are not explicitly mentioned
        # This would be enhanced with NER models in production
        technologies = []
        # Placeholder - would use advanced NLP in production
        return technologies
    
    def extract_location(self, text: str, companies: List[Dict]) -> List[Dict[str, Any]]:
        """Extract Location entities from company data."""
        locations = {}
        
        for company in companies:
            loc_name = company.get("location", "Unknown")
            if loc_name not in locations:
                locations[loc_name] = {
                    "city": loc_name,
                    "country": self._infer_country(loc_name),
                    "office_type": "Headquarters"  # Simplified
                }
        
        return list(locations.values())
    
    def extract_team(self, text: str) -> List[Dict[str, Any]]:
        """Extract Team entities from text."""
        # Teams are not explicitly mentioned in the current dataset
        # Would be enhanced with pattern matching or NER
        teams = []
        return teams
    
    def extract_product(self, text: str) -> List[Dict[str, Any]]:
        """Extract Product entities from text."""
        # Products are not explicitly mentioned in the current dataset
        products = []
        return products
    
    def extract_client(self, text: str) -> List[Dict[str, Any]]:
        """Extract Client entities from text."""
        # Clients are not explicitly mentioned in the current dataset
        clients = []
        return clients
    
    def extract_all(self, text: str) -> Dict[str, List[Dict[str, Any]]]:
        """Extract all entity types from text."""
        # Extract entities that can be directly extracted
        persons = self.extract_person(text)
        companies = self.extract_company(text)
        projects = self.extract_project(text)
        
        # Extract entities derived from other entities
        departments = self.extract_department(text, persons)
        positions = self.extract_position(text, persons)
        locations = self.extract_location(text, companies)
        
        # Extract entities that require advanced NLP (placeholders)
        technologies = self.extract_technology(text)
        teams = self.extract_team(text)
        products = self.extract_product(text)
        clients = self.extract_client(text)
        
        return {
            "Person": persons,
            "Company": companies,
            "Project": projects,
            "Department": departments,
            "Position": positions,
            "Technology": technologies,
            "Location": locations,
            "Team": teams,
            "Product": products,
            "Client": clients
        }
    
    def _infer_department(self, position: str, company: str) -> str:
        """Infer department from position and company."""
        position_lower = position.lower()
        if "engineer" in position_lower or "developer" in position_lower:
            return "Engineering"
        elif "manager" in position_lower or "director" in position_lower:
            return "Management"
        elif "designer" in position_lower or "creative" in position_lower:
            return "Design"
        elif "scientist" in position_lower or "researcher" in position_lower:
            return "R&D"
        elif "architect" in position_lower or "specialist" in position_lower:
            return "IT"
        elif "administrator" in position_lower or "support" in position_lower:
            return "Operations"
        else:
            return "General"
    
    def _infer_location(self, company_name: str) -> str:
        """Infer location from company name (simplified)."""
        # In production, would use knowledge base or geocoding
        location_map = {
            "OpenAI": "San Francisco",
            "Google": "Mountain View",
            "Microsoft": "Redmond",
            "Apple": "Cupertino",
            "Amazon": "Seattle",
            "Meta": "Menlo Park",
            "Tesla": "Palo Alto",
            "Netflix": "Los Gatos",
            "Spotify": "Stockholm",
            "Uber": "San Francisco",
            "IBM": "Armonk",
            "Oracle": "Redwood City",
            "Salesforce": "San Francisco",
            "Adobe": "San Jose",
            "Intel": "Santa Clara",
            "Cisco": "San Jose",
            "HP": "Palo Alto",
            "Dell": "Round Rock",
            "VMware": "Palo Alto",
            "RedHat": "Raleigh"
        }
        return location_map.get(company_name, "Unknown")
    
    def _determine_project_status(self, start_date: str, end_date: str) -> str:
        """Determine project status based on dates."""
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            now = datetime.now()
            
            if now < start:
                return "Planned"
            elif start <= now <= end:
                return "Ongoing"
            else:
                return "Completed"
        except:
            return "Unknown"
    
    def _estimate_budget(self, project_name: str, start_date: str, end_date: str) -> int:
        """Estimate project budget (simplified)."""
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            days = (end - start).days
            # Rough estimate: $1000 per day
            return max(10000, days * 1000)
        except:
            return 100000
    
    def _infer_level(self, position: str) -> str:
        """Infer position level from title."""
        position_lower = position.lower()
        if "senior" in position_lower or "lead" in position_lower or "principal" in position_lower:
            return "Senior"
        elif "junior" in position_lower or "associate" in position_lower:
            return "Junior"
        elif "manager" in position_lower or "director" in position_lower:
            return "Management"
        else:
            return "Mid"
    
    def _estimate_salary_range(self, position: str) -> str:
        """Estimate salary range for position (simplified)."""
        position_lower = position.lower()
        if "senior" in position_lower or "lead" in position_lower:
            return "$120k-$180k"
        elif "manager" in position_lower or "director" in position_lower:
            return "$150k-$250k"
        elif "engineer" in position_lower or "developer" in position_lower:
            return "$90k-$150k"
        else:
            return "$70k-$120k"
    
    def _infer_country(self, city: str) -> str:
        """Infer country from city name."""
        us_cities = ["San Francisco", "Mountain View", "Redmond", "Cupertino", 
                     "Seattle", "Menlo Park", "Palo Alto", "Los Gatos",
                     "Redwood City", "San Jose", "Santa Clara", "Round Rock", "Raleigh"]
        if city in us_cities:
            return "USA"
        elif city == "Stockholm":
            return "Sweden"
        else:
            return "Unknown"


def extract_entities(documents_path: str, entities_schema_path: str, output_path: str):
    """
    Main function to extract entities from documents.
    
    Args:
        documents_path: Path to documents.txt
        entities_schema_path: Path to entities.json
        output_path: Path to save entities_output.json
    """
    # Load schema
    with open(entities_schema_path, 'r', encoding='utf-8') as f:
        entities_schema = json.load(f)
    
    # Load documents
    with open(documents_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Extract entities
    extractor = EntityExtractor(entities_schema)
    entities = extractor.extract_all(text)
    
    # Save output
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(entities, f, indent=2, ensure_ascii=False)
    
    print(f"Extracted entities saved to {output_path}")
    return entities


if __name__ == "__main__":
    extract_entities("documents.txt", "entities.json", "entities_output.json")

