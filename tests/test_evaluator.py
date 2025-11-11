"""
Tests for evaluation framework.
"""

import pytest
import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from evaluator import Evaluator, evaluate_extraction


class TestEvaluator:
    """Test cases for evaluator."""
    
    @pytest.fixture
    def entities_schema(self):
        """Load entities schema."""
        schema_path = Path(__file__).parent.parent / "entities.json"
        with open(schema_path, 'r') as f:
            return json.load(f)
    
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
            ]
        }
    
    @pytest.fixture
    def sample_relations(self):
        """Sample extracted relations."""
        return {
            "WorksAt": [
                {"person": "John Doe", "company": "OpenAI"}
            ]
        }
    
    def test_evaluator_initialization(self, entities_schema, relations_schema):
        """Test Evaluator initialization."""
        evaluator = Evaluator(entities_schema, relations_schema)
        assert evaluator.entities_schema == entities_schema
        assert evaluator.relations_schema == relations_schema
    
    def test_evaluate_entities(self, entities_schema, relations_schema, sample_entities):
        """Test entity evaluation."""
        evaluator = Evaluator(entities_schema, relations_schema)
        metrics = evaluator.evaluate_entities(sample_entities)
        
        assert "entity_f1" in metrics
        assert "entity_precision" in metrics
        assert "entity_recall" in metrics
        assert "entity_schema_compliance" in metrics
        assert 0.0 <= metrics["entity_f1"] <= 1.0
    
    def test_evaluate_relations(self, entities_schema, relations_schema, sample_relations, sample_entities):
        """Test relation evaluation."""
        evaluator = Evaluator(entities_schema, relations_schema)
        metrics = evaluator.evaluate_relations(sample_relations, sample_entities)
        
        assert "relation_f1" in metrics
        assert "relation_precision" in metrics
        assert "relation_recall" in metrics
        assert "relation_schema_compliance" in metrics
        assert "relation_logical_consistency" in metrics
        assert 0.0 <= metrics["relation_f1"] <= 1.0
    
    def test_evaluate_comprehensive(self, entities_schema, relations_schema, sample_entities, sample_relations):
        """Test comprehensive evaluation."""
        evaluator = Evaluator(entities_schema, relations_schema)
        report = evaluator.evaluate(sample_entities, sample_relations, "Test Method")
        
        assert "method" in report
        assert "timestamp" in report
        assert "entity_f1" in report
        assert "relation_f1" in report
        assert "schema_compliance" in report
        assert report["method"] == "Test Method"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

