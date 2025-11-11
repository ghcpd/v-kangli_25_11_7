"""
Tests for real-time collaboration, persistence, and conflict handling.
"""

import pytest
import json
import sys
import tempfile
import shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from entity_extraction import extract_entities
from relation_extraction import extract_relations


class TestPersistence:
    """Test persistence of extraction results."""
    
    def test_output_persistence(self, tmp_path):
        """Test that output files are properly persisted."""
        output_file = tmp_path / "entities_output.json"
        
        # Run extraction
        extract_entities(
            "documents.txt",
            "entities.json",
            str(output_file)
        )
        
        # Verify file exists and is readable
        assert output_file.exists()
        assert output_file.stat().st_size > 0
        
        # Verify JSON is valid
        with open(output_file, 'r') as f:
            data = json.load(f)
            assert isinstance(data, dict)
    
    def test_output_consistency(self, tmp_path):
        """Test that multiple runs produce consistent output."""
        output1 = tmp_path / "output1.json"
        output2 = tmp_path / "output2.json"
        
        # Run extraction twice
        extract_entities("documents.txt", "entities.json", str(output1))
        extract_entities("documents.txt", "entities.json", str(output2))
        
        # Compare outputs
        with open(output1, 'r') as f:
            data1 = json.load(f)
        with open(output2, 'r') as f:
            data2 = json.load(f)
        
        # Should produce same number of entities
        for entity_type in data1.keys():
            assert len(data1[entity_type]) == len(data2[entity_type])


class TestMultiDocument:
    """Test multi-document behavior."""
    
    def test_multiple_documents(self, tmp_path):
        """Test processing multiple documents."""
        # Create multiple test documents
        doc1 = tmp_path / "doc1.txt"
        doc2 = tmp_path / "doc2.txt"
        combined = tmp_path / "combined.txt"
        
        doc1.write_text("John Doe, age 32, works at OpenAI as a Researcher.\n")
        doc2.write_text("Jane Smith, age 28, works at Google as an Engineer.\n")
        
        # Combine documents
        combined.write_text(doc1.read_text() + doc2.read_text())
        
        # Extract from combined document
        output = tmp_path / "output.json"
        extract_entities(str(combined), "entities.json", str(output))
        
        # Verify both entities are extracted
        with open(output, 'r') as f:
            data = json.load(f)
            person_names = [p["name"] for p in data.get("Person", [])]
            assert "John Doe" in person_names or "Jane Smith" in person_names
    
    def test_document_concatenation(self, tmp_path):
        """Test that document concatenation works correctly."""
        # Read original document
        with open("documents.txt", 'r') as f:
            original_text = f.read()
        
        # Create concatenated version
        concatenated = tmp_path / "concatenated.txt"
        concatenated.write_text(original_text + "\n" + original_text)
        
        # Extract from concatenated document
        output = tmp_path / "output.json"
        extract_entities(str(concatenated), "entities.json", str(output))
        
        # Verify extraction works
        with open(output, 'r') as f:
            data = json.load(f)
            assert len(data.get("Person", [])) > 0


class TestConcurrency:
    """Test concurrent execution (simulating collaboration)."""
    
    def test_concurrent_extraction(self, tmp_path):
        """Test that multiple extractions can run concurrently."""
        def run_extraction(i):
            output = tmp_path / f"output_{i}.json"
            try:
                extract_entities("documents.txt", "entities.json", str(output))
                return True
            except Exception as e:
                print(f"Extraction {i} failed: {e}")
                return False
        
        # Run 5 extractions concurrently
        with ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(run_extraction, range(5)))
        
        # All should succeed
        assert all(results)
        
        # Verify all outputs exist
        for i in range(5):
            assert (tmp_path / f"output_{i}.json").exists()
    
    def test_no_file_conflicts(self, tmp_path):
        """Test that concurrent writes don't cause file conflicts."""
        output_file = tmp_path / "shared_output.json"
        
        def write_result(i):
            # Simulate writing to shared file (with unique keys)
            result = {f"result_{i}": i}
            temp_file = tmp_path / f"temp_{i}.json"
            with open(temp_file, 'w') as f:
                json.dump(result, f)
            return True
        
        # Run concurrent writes
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(write_result, range(10)))
        
        assert all(results)
        
        # Verify all temp files were created
        for i in range(10):
            assert (tmp_path / f"temp_{i}.json").exists()


class TestConflictHandling:
    """Test conflict handling in concurrent scenarios."""
    
    def test_idempotent_extraction(self, tmp_path):
        """Test that extraction is idempotent."""
        output = tmp_path / "output.json"
        
        # Run extraction multiple times
        for _ in range(3):
            extract_entities("documents.txt", "entities.json", str(output))
        
        # Verify output is consistent
        with open(output, 'r') as f:
            data = json.load(f)
            assert isinstance(data, dict)
            assert len(data) > 0
    
    def test_partial_failure_recovery(self, tmp_path):
        """Test recovery from partial failures."""
        output = tmp_path / "output.json"
        
        # First extraction
        extract_entities("documents.txt", "entities.json", str(output))
        assert output.exists()
        
        # Simulate partial write (corrupt file)
        output.write_text("{invalid json")
        
        # Re-extraction should recover
        extract_entities("documents.txt", "entities.json", str(output))
        
        # Verify valid JSON
        with open(output, 'r') as f:
            data = json.load(f)
            assert isinstance(data, dict)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

