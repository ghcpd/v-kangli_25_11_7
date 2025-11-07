"""
Evaluation Framework for KGEB (Enterprise Knowledge Graph Extraction Benchmark)

This module provides metrics and evaluation capabilities for entity and relation extraction,
including precision, recall, F1 score, and schema compliance checking.
"""

import json
from typing import Dict, List, Any, Tuple, Set
from datetime import datetime
from dataclasses import dataclass, asdict


@dataclass
class ExtractionMetrics:
    """Metrics for entity or relation extraction."""
    precision: float
    recall: float
    f1_score: float
    true_positives: int
    false_positives: int
    false_negatives: int


class SchemaValidator:
    """Validates schema compliance of extracted entities and relations."""
    
    def __init__(self, entity_schema: str, relation_schema: str):
        """Initialize validator with schema files."""
        self.entity_schema = self._load_schema(entity_schema)
        self.relation_schema = self._load_schema(relation_schema)
    
    def _load_schema(self, schema_path: str) -> Dict[str, Any]:
        """Load schema from JSON file."""
        try:
            with open(schema_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Schema file not found: {schema_path}")
            return {}
    
    def validate_entities(self, entities: Dict[str, List[Dict[str, Any]]]) -> Tuple[bool, Dict[str, Any]]:
        """
        Validate extracted entities against schema.
        
        Args:
            entities: Extracted entities
            
        Returns:
            Tuple of (is_valid, validation_details)
        """
        issues = []
        stats = {
            'total_entities': 0,
            'valid_entities': 0,
            'invalid_entities': 0,
            'missing_attributes': 0,
            'extra_entities': 0
        }
        
        for entity_type, entity_list in entities.items():
            if entity_type not in self.entity_schema:
                stats['extra_entities'] += len(entity_list)
                issues.append(f"Unexpected entity type: {entity_type}")
                continue
            
            required_attributes = self.entity_schema[entity_type]
            
            for entity in entity_list:
                stats['total_entities'] += 1
                missing_attrs = []
                
                for attr in required_attributes:
                    if attr not in entity or entity[attr] is None:
                        missing_attrs.append(attr)
                
                if missing_attrs:
                    stats['missing_attributes'] += len(missing_attrs)
                    stats['invalid_entities'] += 1
                else:
                    stats['valid_entities'] += 1
        
        is_valid = stats['invalid_entities'] == 0 and stats['extra_entities'] == 0
        
        return is_valid, {
            'is_valid': is_valid,
            'stats': stats,
            'issues': issues
        }
    
    def validate_relations(self, relations: Dict[str, List[Dict[str, Any]]]) -> Tuple[bool, Dict[str, Any]]:
        """
        Validate extracted relations against schema.
        
        Args:
            relations: Extracted relations
            
        Returns:
            Tuple of (is_valid, validation_details)
        """
        issues = []
        stats = {
            'total_relations': 0,
            'valid_relations': 0,
            'invalid_relations': 0,
            'unexpected_types': 0
        }
        
        valid_relation_types = {rel['id'] for rel in self.relation_schema.get('relations', [])}
        
        for relation_type, relation_list in relations.items():
            if relation_type not in valid_relation_types:
                stats['unexpected_types'] += len(relation_list)
                issues.append(f"Unexpected relation type: {relation_type}")
                continue
            
            for relation in relation_list:
                stats['total_relations'] += 1
                
                # Check that relation has required fields (typically source and target entities)
                if relation:  # Non-empty relation dict
                    stats['valid_relations'] += 1
                else:
                    stats['invalid_relations'] += 1
        
        is_valid = stats['invalid_relations'] == 0 and stats['unexpected_types'] == 0
        
        return is_valid, {
            'is_valid': is_valid,
            'stats': stats,
            'issues': issues
        }


class EntityEvaluator:
    """Evaluator for entity extraction tasks."""
    
    @staticmethod
    def calculate_metrics(
        gold_entities: Dict[str, List[Dict[str, Any]]],
        predicted_entities: Dict[str, List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        """
        Calculate evaluation metrics for entity extraction.
        
        Args:
            gold_entities: Ground truth entities
            predicted_entities: Predicted entities
            
        Returns:
            Metrics dictionary with precision, recall, F1
        """
        metrics = {}
        overall_tp = 0
        overall_fp = 0
        overall_fn = 0
        
        all_types = set(gold_entities.keys()) | set(predicted_entities.keys())
        
        for entity_type in all_types:
            gold = set()
            pred = set()
            
            # Convert entities to comparable sets
            for entity in gold_entities.get(entity_type, []):
                # Create a hashable representation
                entity_tuple = tuple(sorted(entity.items()))
                gold.add(entity_tuple)
            
            for entity in predicted_entities.get(entity_type, []):
                entity_tuple = tuple(sorted(entity.items()))
                pred.add(entity_tuple)
            
            tp = len(gold & pred)
            fp = len(pred - gold)
            fn = len(gold - pred)
            
            overall_tp += tp
            overall_fp += fp
            overall_fn += fn
            
            # Calculate per-type metrics
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
            
            metrics[entity_type] = {
                'precision': round(precision, 4),
                'recall': round(recall, 4),
                'f1_score': round(f1, 4),
                'tp': tp,
                'fp': fp,
                'fn': fn
            }
        
        # Calculate overall metrics
        overall_precision = overall_tp / (overall_tp + overall_fp) if (overall_tp + overall_fp) > 0 else 0
        overall_recall = overall_tp / (overall_tp + overall_fn) if (overall_tp + overall_fn) > 0 else 0
        overall_f1 = 2 * (overall_precision * overall_recall) / (overall_precision + overall_recall) \
                     if (overall_precision + overall_recall) > 0 else 0
        
        metrics['overall'] = {
            'precision': round(overall_precision, 4),
            'recall': round(overall_recall, 4),
            'f1_score': round(overall_f1, 4),
            'tp': overall_tp,
            'fp': overall_fp,
            'fn': overall_fn
        }
        
        return metrics


class RelationEvaluator:
    """Evaluator for relation extraction tasks."""
    
    @staticmethod
    def calculate_metrics(
        gold_relations: Dict[str, List[Dict[str, Any]]],
        predicted_relations: Dict[str, List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        """
        Calculate evaluation metrics for relation extraction.
        
        Args:
            gold_relations: Ground truth relations
            predicted_relations: Predicted relations
            
        Returns:
            Metrics dictionary with precision, recall, F1
        """
        metrics = {}
        overall_tp = 0
        overall_fp = 0
        overall_fn = 0
        
        all_types = set(gold_relations.keys()) | set(predicted_relations.keys())
        
        for relation_type in all_types:
            gold = set()
            pred = set()
            
            # Convert relations to comparable sets
            for relation in gold_relations.get(relation_type, []):
                rel_tuple = tuple(sorted(relation.items()))
                gold.add(rel_tuple)
            
            for relation in predicted_relations.get(relation_type, []):
                rel_tuple = tuple(sorted(relation.items()))
                pred.add(rel_tuple)
            
            tp = len(gold & pred)
            fp = len(pred - gold)
            fn = len(gold - pred)
            
            overall_tp += tp
            overall_fp += fp
            overall_fn += fn
            
            # Calculate per-type metrics
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
            
            if gold or pred:  # Only include if there are gold or predicted relations
                metrics[relation_type] = {
                    'precision': round(precision, 4),
                    'recall': round(recall, 4),
                    'f1_score': round(f1, 4),
                    'tp': tp,
                    'fp': fp,
                    'fn': fn
                }
        
        # Calculate overall metrics
        overall_precision = overall_tp / (overall_tp + overall_fp) if (overall_tp + overall_fp) > 0 else 0
        overall_recall = overall_tp / (overall_tp + overall_fn) if (overall_tp + overall_fn) > 0 else 0
        overall_f1 = 2 * (overall_precision * overall_recall) / (overall_precision + overall_recall) \
                     if (overall_precision + overall_recall) > 0 else 0
        
        metrics['overall'] = {
            'precision': round(overall_precision, 4),
            'recall': round(overall_recall, 4),
            'f1_score': round(overall_f1, 4),
            'tp': overall_tp,
            'fp': overall_fp,
            'fn': overall_fn
        }
        
        return metrics


class EvaluationReport:
    """Generates comprehensive evaluation reports."""
    
    @staticmethod
    def generate_report(
        method_name: str,
        entity_metrics: Dict[str, Any],
        relation_metrics: Dict[str, Any],
        schema_compliance: Dict[str, Any],
        output_file: str = "evaluation_report.json"
    ) -> Dict[str, Any]:
        """
        Generate comprehensive evaluation report.
        
        Args:
            method_name: Name of the extraction method
            entity_metrics: Entity extraction metrics
            relation_metrics: Relation extraction metrics
            schema_compliance: Schema compliance results
            output_file: Path to save the report
            
        Returns:
            Report dictionary
        """
        report = {
            "method": method_name,
            "timestamp": datetime.now().isoformat() + "Z",
            "entity_metrics": {
                "overall_precision": entity_metrics.get('overall', {}).get('precision', 0),
                "overall_recall": entity_metrics.get('overall', {}).get('recall', 0),
                "overall_f1": entity_metrics.get('overall', {}).get('f1_score', 0),
                "by_type": {
                    k: v for k, v in entity_metrics.items() if k != 'overall'
                }
            },
            "relation_metrics": {
                "overall_precision": relation_metrics.get('overall', {}).get('precision', 0),
                "overall_recall": relation_metrics.get('overall', {}).get('recall', 0),
                "overall_f1": relation_metrics.get('overall', {}).get('f1_score', 0),
                "by_type": {
                    k: v for k, v in relation_metrics.items() if k != 'overall'
                }
            },
            "schema_compliance": schema_compliance,
            "summary": {
                "entity_f1": round(entity_metrics.get('overall', {}).get('f1_score', 0), 4),
                "relation_f1": round(relation_metrics.get('overall', {}).get('f1_score', 0), 4),
                "schema_compliance": f"{schema_compliance.get('entity_compliance', 0):.1%}"
            }
        }
        
        # Save report
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return report
    
    @staticmethod
    def print_report(report: Dict[str, Any]) -> None:
        """Pretty print evaluation report."""
        print("\n" + "="*60)
        print(f"KGEB Evaluation Report - {report['method']}")
        print("="*60)
        print(f"Timestamp: {report['timestamp']}")
        print()
        
        print("Entity Extraction Metrics:")
        print(f"  Precision: {report['entity_metrics']['overall_precision']:.4f}")
        print(f"  Recall:    {report['entity_metrics']['overall_recall']:.4f}")
        print(f"  F1 Score:  {report['entity_metrics']['overall_f1']:.4f}")
        print()
        
        print("Relation Extraction Metrics:")
        print(f"  Precision: {report['relation_metrics']['overall_precision']:.4f}")
        print(f"  Recall:    {report['relation_metrics']['overall_recall']:.4f}")
        print(f"  F1 Score:  {report['relation_metrics']['overall_f1']:.4f}")
        print()
        
        print("Schema Compliance:")
        print(f"  {report['summary']['schema_compliance']}")
        print()
        
        print("="*60)
