"""
Tests for entity extraction module.
"""

import pytest
import json
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from entity_extraction import EntityExtractor, extract_entities


class TestEntityExtraction:
    """Test cases for entity extraction."""
    
    @pytest.fixture
    def entities_schema(self):
        """Load entities schema."""
        schema_path = Path(__file__).parent.parent / "entities.json"
        with open(schema_path, 'r') as f:
            return json.load(f)
    
    @pytest.fixture
    def sample_text(self):
        """Sample enterprise text for testing."""
        return """
        John Doe, age 32, works at OpenAI as a Researcher.
        Jane Smith, age 28, works at Google as an Engineer.
        OpenAI operates in the Technology industry.
        Project Alpha started on 2023-01-15, ends on 2023-06-30.
        """
    
    def test_entity_extractor_initialization(self, entities_schema):
        """Test EntityExtractor initialization."""
        extractor = EntityExtractor(entities_schema)
        assert extractor.entities_schema == entities_schema
        assert len(extractor.extracted_entities) == len(entities_schema)
    
    def test_extract_person(self, entities_schema, sample_text):
        """Test person extraction."""
        extractor = EntityExtractor(entities_schema)
        persons = extractor.extract_person(sample_text)
        
        assert len(persons) >= 2
        assert any(p["name"] == "John Doe" for p in persons)
        assert any(p["name"] == "Jane Smith" for p in persons)
        
        # Check required attributes
        for person in persons:
            assert "name" in person
            assert "age" in person
            assert "position" in person
            assert "department" in person
    
    def test_extract_company(self, entities_schema, sample_text):
        """Test company extraction."""
        extractor = EntityExtractor(entities_schema)
        companies = extractor.extract_company(sample_text)
        
        assert len(companies) >= 1
        assert any(c["name"] == "OpenAI" for c in companies)
        
        # Check required attributes
        for company in companies:
            assert "name" in company
            assert "industry" in company
            assert "sector" in company
            assert "location" in company
    
    def test_extract_project(self, entities_schema, sample_text):
        """Test project extraction."""
        extractor = EntityExtractor(entities_schema)
        projects = extractor.extract_project(sample_text)
        
        assert len(projects) >= 1
        assert any(p["name"] == "Alpha" for p in projects)
        
        # Check required attributes
        for project in projects:
            assert "name" in project
            assert "start_date" in project
            assert "end_date" in project
            assert "status" in project
            assert "budget" in project
    
    def test_extract_all(self, entities_schema, sample_text):
        """Test extraction of all entity types."""
        extractor = EntityExtractor(entities_schema)
        entities = extractor.extract_all(sample_text)
        
        # Check all entity types are present
        for entity_type in entities_schema.keys():
            assert entity_type in entities
            assert isinstance(entities[entity_type], list)
    
    def test_schema_compliance(self, entities_schema, sample_text):
        """Test that extracted entities comply with schema."""
        extractor = EntityExtractor(entities_schema)
        entities = extractor.extract_all(sample_text)
        
        for entity_type, attributes in entities_schema.items():
            for entity in entities[entity_type]:
                # Check all required attributes are present
                for attr in attributes:
                    assert attr in entity, f"Missing attribute {attr} in {entity_type}"


class TestEntityExtractionIntegration:
    """Integration tests for entity extraction."""
    
    def test_full_extraction_pipeline(self, tmp_path):
        """Test full extraction pipeline with file I/O."""
        # Create temporary test files
        test_doc = tmp_path / "test_documents.txt"
        test_schema = tmp_path / "test_entities.json"
        test_output = tmp_path / "test_output.json"
        
        # Write test data
        test_doc.write_text("John Doe, age 32, works at OpenAI as a Researcher.\n")
        test_schema.write_text(json.dumps({
            "Person": ["name", "age", "position", "department"]
        }))
        
        # Run extraction
        extract_entities(str(test_doc), str(test_schema), str(test_output))
        
        # Verify output
        assert test_output.exists()
        with open(test_output, 'r') as f:
            output = json.load(f)
            assert "Person" in output
            assert len(output["Person"]) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

