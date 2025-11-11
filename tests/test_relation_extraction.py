"""
Tests for relation extraction module.
"""

import pytest
import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from relation_extraction import RelationExtractor, extract_relations


class TestRelationExtraction:
    """Test cases for relation extraction."""
    
    @pytest.fixture
    def relations_schema(self):
        """Load relations schema."""
        schema_path = Path(__file__).parent.parent / "relations.json"
        with open(schema_path, 'r') as f:
            return json.load(f)
    
    @pytest.fixture
    def sample_entities(self):
        """Sample extracted entities."""
        return {
            "Person": [
                {"name": "John Doe", "age": 32, "position": "Researcher", "department": "R&D"}
            ],
            "Company": [
                {"name": "OpenAI", "industry": "Technology", "sector": "Technology", "location": "San Francisco"}
            ],
            "Project": [
                {"name": "Alpha", "start_date": "2023-01-15", "end_date": "2023-06-30", "status": "Completed", "budget": 100000}
            ]
        }
    
    @pytest.fixture
    def sample_text(self):
        """Sample enterprise text for testing."""
        return """
        John Doe, age 32, works at OpenAI as a Researcher.
        John Doe manages 3 projects: Alpha, Beta, Gamma.
        """
    
    def test_relation_extractor_initialization(self, relations_schema, sample_entities):
        """Test RelationExtractor initialization."""
        extractor = RelationExtractor(relations_schema, sample_entities)
        assert extractor.relations_schema == relations_schema
        assert extractor.entities == sample_entities
    
    def test_extract_works_at(self, relations_schema, sample_entities, sample_text):
        """Test WorksAt relation extraction."""
        extractor = RelationExtractor(relations_schema, sample_entities)
        relations = extractor.extract_works_at(sample_text)
        
        assert len(relations) >= 1
        assert any(r.get("person") == "John Doe" for r in relations)
        assert any(r.get("company") == "OpenAI" for r in relations)
    
    def test_extract_manages_project(self, relations_schema, sample_entities, sample_text):
        """Test ManagesProject relation extraction."""
        extractor = RelationExtractor(relations_schema, sample_entities)
        relations = extractor.extract_manages_project(sample_text)
        
        assert len(relations) >= 1
        assert any(r.get("person") == "John Doe" for r in relations)
        assert any(r.get("project") == "Alpha" for r in relations)
    
    def test_extract_all(self, relations_schema, sample_entities, sample_text):
        """Test extraction of all relation types."""
        extractor = RelationExtractor(relations_schema, sample_entities)
        relations = extractor.extract_all(sample_text)
        
        # Check all relation types are present
        for relation_type in relations_schema.keys():
            assert relation_type in relations
            assert isinstance(relations[relation_type], list)


class TestRelationExtractionIntegration:
    """Integration tests for relation extraction."""
    
    def test_full_extraction_pipeline(self, tmp_path):
        """Test full relation extraction pipeline with file I/O."""
        # Create temporary test files
        test_doc = tmp_path / "test_documents.txt"
        test_relations_schema = tmp_path / "test_relations.json"
        test_entities = tmp_path / "test_entities.json"
        test_output = tmp_path / "test_relations_output.json"
        
        # Write test data
        test_doc.write_text("John Doe, age 32, works at OpenAI as a Researcher.\n")
        test_relations_schema.write_text(json.dumps({
            "WorksAt": {
                "description": "Person works at Company",
                "source_entity": "Person",
                "target_entity": "Company"
            }
        }))
        test_entities.write_text(json.dumps({
            "Person": [{"name": "John Doe", "age": 32, "position": "Researcher", "department": "R&D"}],
            "Company": [{"name": "OpenAI", "industry": "Technology", "sector": "Technology", "location": "San Francisco"}]
        }))
        
        # Run extraction
        extract_relations(str(test_doc), str(test_relations_schema), str(test_entities), str(test_output))
        
        # Verify output
        assert test_output.exists()
        with open(test_output, 'r') as f:
            output = json.load(f)
            assert "WorksAt" in output


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

