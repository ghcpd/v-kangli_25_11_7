"""
Test Report Templates and Generators for KGEB

Provides structured templates for test analysis and reporting.
"""

import json
from datetime import datetime
from typing import Dict, Any, List
from pathlib import Path


class TestReportTemplate:
    """Base template for test reports."""
    
    @staticmethod
    def create_minimal_report(
        test_name: str,
        status: str,
        duration: float,
        message: str = ""
    ) -> Dict[str, Any]:
        """
        Create a minimal test report.
        
        Args:
            test_name: Name of the test
            status: Test status (passed/failed/skipped)
            duration: Test execution duration in seconds
            message: Optional message
            
        Returns:
            Report dictionary
        """
        return {
            "test_name": test_name,
            "status": status,
            "duration": duration,
            "timestamp": datetime.now().isoformat() + "Z",
            "message": message
        }
    
    @staticmethod
    def create_detailed_report(
        test_name: str,
        status: str,
        duration: float,
        category: str,
        assertions: Dict[str, bool],
        details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a detailed test report with assertions.
        
        Args:
            test_name: Name of the test
            status: Test status
            duration: Execution duration
            category: Test category (reproducibility, persistence, etc.)
            assertions: Dictionary of assertion results
            details: Additional details
            
        Returns:
            Detailed report dictionary
        """
        passed_assertions = sum(1 for v in assertions.values() if v)
        total_assertions = len(assertions)
        
        return {
            "test_name": test_name,
            "status": status,
            "category": category,
            "duration": duration,
            "timestamp": datetime.now().isoformat() + "Z",
            "assertions": {
                "passed": passed_assertions,
                "total": total_assertions,
                "details": assertions
            },
            "details": details
        }


class ReproducibilityReportTemplate:
    """Template for reproducibility test reports."""
    
    @staticmethod
    def create_report(
        runs: int,
        identical: bool,
        variance: float = 0.0,
        details: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Create reproducibility report.
        
        Args:
            runs: Number of runs
            identical: Whether all runs produced identical results
            variance: Variance across runs (if applicable)
            details: Additional details
            
        Returns:
            Report dictionary
        """
        return {
            "report_type": "reproducibility",
            "timestamp": datetime.now().isoformat() + "Z",
            "summary": {
                "runs": runs,
                "identical_results": identical,
                "variance": variance,
                "status": "passed" if identical else "failed"
            },
            "details": details or {}
        }


class PersistenceReportTemplate:
    """Template for persistence test reports."""
    
    @staticmethod
    def create_report(
        test_cases: List[Dict[str, Any]],
        success_rate: float,
        total_tests: int
    ) -> Dict[str, Any]:
        """
        Create persistence report.
        
        Args:
            test_cases: List of test case results
            success_rate: Success rate percentage
            total_tests: Total number of tests
            
        Returns:
            Report dictionary
        """
        return {
            "report_type": "persistence",
            "timestamp": datetime.now().isoformat() + "Z",
            "summary": {
                "total_tests": total_tests,
                "success_rate": round(success_rate * 100, 2),
                "status": "passed" if success_rate == 1.0 else "failed"
            },
            "test_cases": test_cases
        }


class ConflictHandlingReportTemplate:
    """Template for conflict handling test reports."""
    
    @staticmethod
    def create_report(
        duplicates_detected: int,
        duplicates_handled: int,
        conflicts_resolved: int,
        total_entities: int
    ) -> Dict[str, Any]:
        """
        Create conflict handling report.
        
        Args:
            duplicates_detected: Number of duplicates detected
            duplicates_handled: Number of duplicates properly handled
            conflicts_resolved: Number of conflicts resolved
            total_entities: Total entities processed
            
        Returns:
            Report dictionary
        """
        handling_rate = duplicates_handled / max(duplicates_detected, 1)
        
        return {
            "report_type": "conflict_handling",
            "timestamp": datetime.now().isoformat() + "Z",
            "summary": {
                "total_entities": total_entities,
                "duplicates_detected": duplicates_detected,
                "duplicates_handled": duplicates_handled,
                "handling_rate": round(handling_rate * 100, 2),
                "conflicts_resolved": conflicts_resolved,
                "status": "passed" if handling_rate == 1.0 else "failed"
            }
        }


class MultiDocumentReportTemplate:
    """Template for multi-document test reports."""
    
    @staticmethod
    def create_report(
        documents_processed: int,
        total_entities_extracted: int,
        total_relations_extracted: int,
        consistency_score: float
    ) -> Dict[str, Any]:
        """
        Create multi-document report.
        
        Args:
            documents_processed: Number of documents
            total_entities_extracted: Total entities across all documents
            total_relations_extracted: Total relations across all documents
            consistency_score: Score from 0 to 1 indicating consistency
            
        Returns:
            Report dictionary
        """
        return {
            "report_type": "multi_document",
            "timestamp": datetime.now().isoformat() + "Z",
            "summary": {
                "documents_processed": documents_processed,
                "total_entities_extracted": total_entities_extracted,
                "total_relations_extracted": total_relations_extracted,
                "entities_per_document": round(total_entities_extracted / max(documents_processed, 1), 2),
                "relations_per_document": round(total_relations_extracted / max(documents_processed, 1), 2),
                "consistency_score": round(consistency_score, 4),
                "status": "passed" if consistency_score >= 0.9 else "failed"
            }
        }


class SchemaComplianceReportTemplate:
    """Template for schema compliance test reports."""
    
    @staticmethod
    def create_report(
        schema_type: str,
        total_items: int,
        compliant_items: int,
        violations: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Create schema compliance report.
        
        Args:
            schema_type: Type of schema (entity/relation)
            total_items: Total items checked
            compliant_items: Items compliant with schema
            violations: List of violations
            
        Returns:
            Report dictionary
        """
        compliance_rate = compliant_items / max(total_items, 1)
        
        return {
            "report_type": "schema_compliance",
            "schema_type": schema_type,
            "timestamp": datetime.now().isoformat() + "Z",
            "summary": {
                "total_items": total_items,
                "compliant_items": compliant_items,
                "compliance_rate": round(compliance_rate * 100, 2),
                "violations": len(violations),
                "status": "passed" if compliance_rate == 1.0 else "failed"
            },
            "violations": violations
        }


class ComprehensiveTestReportTemplate:
    """Template for comprehensive test suite report."""
    
    @staticmethod
    def create_report(
        reproducibility: Dict[str, Any],
        persistence: Dict[str, Any],
        conflict_handling: Dict[str, Any],
        multi_document: Dict[str, Any],
        schema_compliance: Dict[str, Any],
        integration: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create comprehensive test report.
        
        Args:
            reproducibility: Reproducibility test results
            persistence: Persistence test results
            conflict_handling: Conflict handling test results
            multi_document: Multi-document test results
            schema_compliance: Schema compliance test results
            integration: Integration test results
            
        Returns:
            Comprehensive report dictionary
        """
        test_suites = {
            "reproducibility": reproducibility,
            "persistence": persistence,
            "conflict_handling": conflict_handling,
            "multi_document": multi_document,
            "schema_compliance": schema_compliance,
            "integration": integration
        }
        
        passed_suites = sum(1 for suite in test_suites.values() 
                           if suite.get('summary', {}).get('status') == 'passed')
        total_suites = len(test_suites)
        
        return {
            "report_type": "comprehensive_test_report",
            "timestamp": datetime.now().isoformat() + "Z",
            "kgeb_version": "1.0.0",
            "overall_summary": {
                "total_test_suites": total_suites,
                "passed_suites": passed_suites,
                "failed_suites": total_suites - passed_suites,
                "overall_status": "passed" if passed_suites == total_suites else "failed",
                "success_rate": round(passed_suites / total_suites * 100, 2)
            },
            "test_suites": test_suites
        }
    
    @staticmethod
    def save_report(report: Dict[str, Any], output_path: str) -> None:
        """
        Save report to file.
        
        Args:
            report: Report dictionary
            output_path: Path to save the report
        """
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def print_report_summary(report: Dict[str, Any]) -> None:
        """Print a summary of the test report."""
        print("\n" + "="*70)
        print("KGEB Comprehensive Test Report Summary")
        print("="*70)
        print(f"Timestamp: {report['timestamp']}")
        print(f"KGEB Version: {report.get('kgeb_version', 'Unknown')}")
        print()
        
        summary = report.get('overall_summary', {})
        print("Overall Results:")
        print(f"  Total Test Suites: {summary.get('total_test_suites', 0)}")
        print(f"  Passed Suites: {summary.get('passed_suites', 0)}")
        print(f"  Failed Suites: {summary.get('failed_suites', 0)}")
        print(f"  Success Rate: {summary.get('success_rate', 0):.1f}%")
        print(f"  Overall Status: {summary.get('overall_status', 'unknown').upper()}")
        print()
        
        print("Test Suite Results:")
        for suite_name, suite_result in report.get('test_suites', {}).items():
            status = suite_result.get('summary', {}).get('status', 'unknown').upper()
            print(f"  - {suite_name}: {status}")
        
        print()
        print("="*70)


# Example usage and templates
TEMPLATE_EXAMPLES = {
    "minimal_test": {
        "test_name": "test_entity_extraction",
        "status": "passed",
        "duration": 0.125,
        "timestamp": "2025-11-07T12:30:00Z",
        "message": "Entity extraction test completed successfully"
    },
    "reproducibility": {
        "report_type": "reproducibility",
        "timestamp": "2025-11-07T12:30:00Z",
        "summary": {
            "runs": 5,
            "identical_results": True,
            "variance": 0.0,
            "status": "passed"
        }
    },
    "persistence": {
        "report_type": "persistence",
        "timestamp": "2025-11-07T12:30:00Z",
        "summary": {
            "total_tests": 10,
            "success_rate": 100.0,
            "status": "passed"
        }
    },
    "conflict_handling": {
        "report_type": "conflict_handling",
        "timestamp": "2025-11-07T12:30:00Z",
        "summary": {
            "total_entities": 100,
            "duplicates_detected": 15,
            "duplicates_handled": 15,
            "handling_rate": 100.0,
            "conflicts_resolved": 12,
            "status": "passed"
        }
    },
    "multi_document": {
        "report_type": "multi_document",
        "timestamp": "2025-11-07T12:30:00Z",
        "summary": {
            "documents_processed": 3,
            "total_entities_extracted": 300,
            "total_relations_extracted": 250,
            "entities_per_document": 100.0,
            "relations_per_document": 83.33,
            "consistency_score": 0.95,
            "status": "passed"
        }
    },
    "schema_compliance": {
        "report_type": "schema_compliance",
        "schema_type": "entity",
        "timestamp": "2025-11-07T12:30:00Z",
        "summary": {
            "total_items": 100,
            "compliant_items": 98,
            "compliance_rate": 98.0,
            "violations": 2,
            "status": "failed"
        }
    }
}


def generate_example_reports(output_dir: str = "reports/templates") -> None:
    """Generate example report templates."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    for report_name, template in TEMPLATE_EXAMPLES.items():
        output_path = Path(output_dir) / f"{report_name}_template.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(template, f, indent=2, ensure_ascii=False)
        print(f"Generated: {output_path}")


if __name__ == '__main__':
    generate_example_reports()
