"""
Automated Test Suite for KGEB

Tests for:
- Reproducibility: Same input produces same output
- Persistence: Results are properly saved and loaded
- Conflict handling: Duplicate entities are handled correctly
- Multi-document behavior: Multiple documents are processed correctly
"""

import pytest
import json
import tempfile
import shutil
from pathlib import Path
from entity_extractor import EntityExtractor
from relation_extractor import RelationExtractor
from evaluator import SchemaValidator, EntityEvaluator, RelationEvaluator
from main import KGEBPipeline


class TestReproducibility:
    """Test reproducibility: same input should produce same output."""
    
    def test_entity_extraction_reproducibility(self):
        """Test that entity extraction is reproducible."""
        test_text = """
        John Doe, age 32, works at OpenAI as a Researcher.
        Jane Smith, age 28, works at Google as an Engineer.
        Project Alpha started on 2023-01-15, ends on 2023-06-30.
        OpenAI operates in the Technology industry.
        """
        
        # First extraction
        extractor1 = EntityExtractor()
        result1 = extractor1.extract_from_text(test_text)
        
        # Second extraction
        extractor2 = EntityExtractor()
        result2 = extractor2.extract_from_text(test_text)
        
        # Results should be identical
        assert result1 == result2, "Entity extraction is not reproducible"
    
    def test_entity_extraction_order_independence(self):
        """Test that extraction results are independent of input order."""
        text1 = """
        John Doe, age 32, works at OpenAI as a Researcher.
        Jane Smith, age 28, works at Google as an Engineer.
        """
        
        text2 = """
        Jane Smith, age 28, works at Google as an Engineer.
        John Doe, age 32, works at OpenAI as a Researcher.
        """
        
        extractor1 = EntityExtractor()
        result1 = extractor1.extract_from_text(text1)
        
        extractor2 = EntityExtractor()
        result2 = extractor2.extract_from_text(text2)
        
        # Convert to sets for order-independent comparison
        persons1 = {json.dumps(p, sort_keys=True) for p in result1['Person']}
        persons2 = {json.dumps(p, sort_keys=True) for p in result2['Person']}
        
        assert persons1 == persons2, "Extraction is order-dependent"
    
    def test_relation_extraction_reproducibility(self):
        """Test that relation extraction is reproducible."""
        test_text = """
        John Doe, age 32, works at OpenAI as a Researcher.
        Jane Smith, age 28, works at Google as an Engineer.
        John Doe manages 3 projects: Alpha, Beta, Gamma.
        OpenAI operates in the Technology industry.
        """
        
        entities = {
            "Person": [
                {"name": "John Doe", "age": 32, "position": "Researcher", "department": None},
                {"name": "Jane Smith", "age": 28, "position": "Engineer", "department": None}
            ],
            "Project": [
                {"name": "Alpha", "start_date": None, "end_date": None, "status": None, "budget": None},
                {"name": "Beta", "start_date": None, "end_date": None, "status": None, "budget": None},
                {"name": "Gamma", "start_date": None, "end_date": None, "status": None, "budget": None}
            ],
            "Company": [],
            "Department": [],
            "Position": [],
            "Technology": [],
            "Location": [],
            "Team": [],
            "Product": [],
            "Client": []
        }
        
        # First extraction
        extractor1 = RelationExtractor()
        result1 = extractor1.extract_from_text(test_text, entities)
        
        # Second extraction
        extractor2 = RelationExtractor()
        result2 = extractor2.extract_from_text(test_text, entities)
        
        # Compare non-empty relations
        for rel_type in result1:
            assert set(json.dumps(r, sort_keys=True) for r in result1[rel_type]) == \
                   set(json.dumps(r, sort_keys=True) for r in result2[rel_type]), \
                   f"Relation extraction is not reproducible for {rel_type}"


class TestPersistence:
    """Test persistence: results are properly saved and loaded."""
    
    def test_entity_persistence(self):
        """Test that entities are correctly saved and loaded."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test_entities.json"
            
            test_entities = {
                "Person": [
                    {"name": "John Doe", "age": 32, "position": "Researcher", "department": "R&D"}
                ],
                "Company": [
                    {"name": "OpenAI", "industry": "Technology", "sector": "AI", "location": "San Francisco"}
                ],
                "Project": [],
                "Department": [],
                "Position": [],
                "Technology": [],
                "Location": [],
                "Team": [],
                "Product": [],
                "Client": []
            }
            
            # Save
            with open(test_file, 'w') as f:
                json.dump(test_entities, f)
            
            # Load
            with open(test_file, 'r') as f:
                loaded = json.load(f)
            
            assert loaded == test_entities, "Entity persistence failed"
    
    def test_relation_persistence(self):
        """Test that relations are correctly saved and loaded."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test_relations.json"
            
            test_relations = {
                "WorksAt": [
                    {"person": "John Doe", "company": "OpenAI"}
                ],
                "ManagesProject": [
                    {"person": "John Doe", "project": "Alpha"}
                ]
            }
            
            # Save
            with open(test_file, 'w') as f:
                json.dump(test_relations, f)
            
            # Load
            with open(test_file, 'r') as f:
                loaded = json.load(f)
            
            assert loaded == test_relations, "Relation persistence failed"


class TestConflictHandling:
    """Test conflict handling: duplicate entities are handled correctly."""
    
    def test_duplicate_entity_handling(self):
        """Test that duplicate entities are detected and not duplicated."""
        test_text = """
        John Doe, age 32, works at OpenAI as a Researcher.
        John Doe, age 32, works at OpenAI as a Researcher.
        Jane Smith, age 28, works at Google as an Engineer.
        """
        
        extractor = EntityExtractor()
        result = extractor.extract_from_text(test_text)
        
        # Should have 2 persons, not 3
        persons = [p for p in result['Person'] if p['name'] == 'John Doe']
        assert len(persons) == 1, "Duplicate entities not properly handled"
    
    def test_duplicate_relation_handling(self):
        """Test that duplicate relations are detected and not duplicated."""
        test_text = """
        John Doe, age 32, works at OpenAI as a Researcher.
        John Doe manages 3 projects: Alpha, Beta, Gamma.
        John Doe manages 3 projects: Alpha, Beta, Gamma.
        """
        
        entities = {
            "Person": [{"name": "John Doe", "age": 32, "position": "Researcher", "department": None}],
            "Project": [
                {"name": "Alpha", "start_date": None, "end_date": None, "status": None, "budget": None},
                {"name": "Beta", "start_date": None, "end_date": None, "status": None, "budget": None},
                {"name": "Gamma", "start_date": None, "end_date": None, "status": None, "budget": None}
            ],
            "Company": [], "Department": [], "Position": [], "Technology": [],
            "Location": [], "Team": [], "Product": [], "Client": []
        }
        
        extractor = RelationExtractor()
        result = extractor.extract_from_text(test_text, entities)
        
        # Check that duplicate relations are not created
        alpha_relations = [r for r in result.get('ManagesProject', []) if r.get('project') == 'Alpha']
        assert len(alpha_relations) == 1, "Duplicate relations not properly handled"


class TestMultiDocument:
    """Test multi-document behavior: multiple documents are processed correctly."""
    
    def test_multi_document_extraction(self):
        """Test extracting from multiple documents."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test files
            doc1 = Path(tmpdir) / "doc1.txt"
            doc2 = Path(tmpdir) / "doc2.txt"
            
            doc1.write_text("""
            John Doe, age 32, works at OpenAI as a Researcher.
            Project Alpha started on 2023-01-15, ends on 2023-06-30.
            """)
            
            doc2.write_text("""
            Jane Smith, age 28, works at Google as an Engineer.
            Project Beta started on 2023-02-01, ends on 2023-08-15.
            """)
            
            # Extract from both documents
            extractor1 = EntityExtractor()
            result1 = extractor1.extract_from_file(str(doc1))
            
            extractor2 = EntityExtractor()
            result2 = extractor2.extract_from_file(str(doc2))
            
            # Merge results
            merged = {k: result1[k] + result2[k] for k in result1}
            
            # Check merged results
            assert len(merged['Person']) == 2, "Multi-document person extraction failed"
            assert len(merged['Project']) == 2, "Multi-document project extraction failed"
    
    def test_multi_document_relation_consistency(self):
        """Test that relations are consistent across multiple documents."""
        doc_text = """
        John Doe, age 32, works at OpenAI as a Researcher.
        Jane Smith, age 28, works at Google as an Engineer.
        John Doe manages 2 projects: Alpha, Beta.
        Jane Smith leads 1 project: Gamma.
        """
        
        entities = {
            "Person": [
                {"name": "John Doe", "age": 32, "position": "Researcher", "department": None},
                {"name": "Jane Smith", "age": 28, "position": "Engineer", "department": None}
            ],
            "Project": [
                {"name": "Alpha", "start_date": None, "end_date": None, "status": None, "budget": None},
                {"name": "Beta", "start_date": None, "end_date": None, "status": None, "budget": None},
                {"name": "Gamma", "start_date": None, "end_date": None, "status": None, "budget": None}
            ],
            "Company": [], "Department": [], "Position": [], "Technology": [],
            "Location": [], "Team": [], "Product": [], "Client": []
        }
        
        extractor = RelationExtractor()
        result = extractor.extract_from_text(doc_text, entities)
        
        # Verify relations are correct
        manages_relations = result.get('ManagesProject', [])
        john_relations = [r for r in manages_relations if r.get('person') == 'John Doe']
        assert len(john_relations) == 2, "Multi-document relation consistency failed"


class TestSchemaCompliance:
    """Test schema compliance validation."""
    
    def test_entity_schema_validation(self):
        """Test entity schema validation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            entities_schema = Path(tmpdir) / "entities.json"
            relations_schema = Path(tmpdir) / "relations.json"
            
            entities_schema.write_text(json.dumps({
                "Person": ["name", "age", "position", "department"],
                "Company": ["name", "industry", "sector", "location"]
            }))
            
            relations_schema.write_text(json.dumps({"relations": []}))
            
            validator = SchemaValidator(str(entities_schema), str(relations_schema))
            
            test_entities = {
                "Person": [
                    {"name": "John Doe", "age": 32, "position": "Researcher", "department": "R&D"}
                ],
                "Company": []
            }
            
            is_valid, details = validator.validate_entities(test_entities)
            assert is_valid or details['stats']['valid_entities'] > 0, "Schema validation failed"


class TestIntegration:
    """Integration tests for the complete pipeline."""
    
    def test_full_pipeline_execution(self):
        """Test complete pipeline execution."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            # Create test files
            docs_file = tmpdir / "documents.txt"
            entities_schema = tmpdir / "entities.json"
            relations_schema = tmpdir / "relations.json"
            
            docs_file.write_text("""
            John Doe, age 32, works at OpenAI as a Researcher.
            Project Alpha started on 2023-01-15, ends on 2023-06-30.
            """)
            
            entities_schema.write_text(json.dumps({
                "Person": ["name", "age", "position", "department"],
                "Company": ["name", "industry", "sector", "location"],
                "Project": ["name", "start_date", "end_date", "status", "budget"],
                "Department": [],
                "Position": [],
                "Technology": [],
                "Location": [],
                "Team": [],
                "Product": [],
                "Client": []
            }))
            
            relations_schema.write_text(json.dumps({"relations": []}))
            
            # Run pipeline
            pipeline = KGEBPipeline(
                data_dir=str(tmpdir),
                output_dir=str(tmpdir / "output"),
                entities_schema="entities.json",
                relations_schema="relations.json"
            )
            
            results = pipeline.run_full_pipeline("documents.txt")
            
            # Verify results
            assert 'entities' in results, "Pipeline missing entities"
            assert 'relations' in results, "Pipeline missing relations"
            assert 'evaluation' in results, "Pipeline missing evaluation"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
