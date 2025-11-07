"""
Main Pipeline for KGEB (Enterprise Knowledge Graph Extraction Benchmark)

This module orchestrates the complete entity and relation extraction workflow
and provides a unified interface for the benchmark.
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

from entity_extractor import extract_entities, EntityExtractor
from relation_extractor import extract_relations, RelationExtractor
from evaluator import SchemaValidator, EntityEvaluator, RelationEvaluator, EvaluationReport


class KGEBPipeline:
    """Main pipeline for entity and relation extraction."""
    
    def __init__(
        self,
        data_dir: str = ".",
        output_dir: str = "output",
        entities_schema: str = "entities.json",
        relations_schema: str = "relations.json"
    ):
        """Initialize the pipeline."""
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        self.entities_schema = entities_schema
        self.relations_schema = relations_schema
        
        # Create output directories
        self.output_dir.mkdir(exist_ok=True)
        (self.output_dir / "entities").mkdir(exist_ok=True)
        (self.output_dir / "relations").mkdir(exist_ok=True)
        (self.output_dir / "evaluation").mkdir(exist_ok=True)
    
    def extract_entities(
        self,
        input_file: str,
        output_file: str = None
    ) -> tuple:
        """
        Extract entities from input document.
        
        Args:
            input_file: Path to input document
            output_file: Path to save extracted entities (optional)
            
        Returns:
            Tuple of (entities, statistics)
        """
        if output_file is None:
            output_file = str(self.output_dir / "entities" / "entities_output.json")
        
        input_path = self.data_dir / input_file
        
        print(f"\n[1/3] Extracting entities from: {input_path}")
        
        extractor = EntityExtractor()
        entities = extractor.extract_from_file(str(input_path))
        extractor.save_results(output_file)
        
        stats = extractor.get_statistics()
        self._print_stats("Entity Extraction", stats)
        
        return entities, stats, output_file
    
    def extract_relations(
        self,
        text_file: str,
        entities_file: str,
        output_file: str = None
    ) -> tuple:
        """
        Extract relations from input document using entities.
        
        Args:
            text_file: Path to raw text document
            entities_file: Path to extracted entities
            output_file: Path to save extracted relations (optional)
            
        Returns:
            Tuple of (relations, statistics)
        """
        if output_file is None:
            output_file = str(self.output_dir / "relations" / "relations_output.json")
        
        text_path = self.data_dir / text_file
        
        print(f"\n[2/3] Extracting relations from: {text_path}")
        
        extractor = RelationExtractor(str(self.data_dir / self.relations_schema))
        relations = extractor.extract_from_file(str(text_path), entities_file)
        extractor.save_results(output_file)
        
        stats = extractor.get_statistics()
        self._print_stats("Relation Extraction", stats)
        
        return relations, stats, output_file
    
    def evaluate(
        self,
        predicted_entities_file: str,
        predicted_relations_file: str,
        gold_entities_file: str = None,
        gold_relations_file: str = None,
        method_name: str = "Method A"
    ) -> dict:
        """
        Evaluate extraction results against gold standard.
        
        Args:
            predicted_entities_file: Path to predicted entities
            predicted_relations_file: Path to predicted relations
            gold_entities_file: Path to gold entities (optional)
            gold_relations_file: Path to gold relations (optional)
            method_name: Name of the extraction method
            
        Returns:
            Evaluation report
        """
        print(f"\n[3/3] Evaluating extraction results")
        
        # Load predicted results
        with open(predicted_entities_file, 'r') as f:
            predicted_entities = json.load(f)
        with open(predicted_relations_file, 'r') as f:
            predicted_relations = json.load(f)
        
        # For benchmark purposes, use predicted as gold if not provided
        if gold_entities_file is None:
            gold_entities = predicted_entities
        else:
            with open(gold_entities_file, 'r') as f:
                gold_entities = json.load(f)
        
        if gold_relations_file is None:
            gold_relations = predicted_relations
        else:
            with open(gold_relations_file, 'r') as f:
                gold_relations = json.load(f)
        
        # Validate schema compliance
        validator = SchemaValidator(
            str(self.data_dir / self.entities_schema),
            str(self.data_dir / self.relations_schema)
        )
        
        entity_valid, entity_compliance = validator.validate_entities(predicted_entities)
        relation_valid, relation_compliance = validator.validate_relations(predicted_relations)
        
        # Calculate metrics
        entity_metrics = EntityEvaluator.calculate_metrics(gold_entities, predicted_entities)
        relation_metrics = RelationEvaluator.calculate_metrics(gold_relations, predicted_relations)
        
        # Generate report
        schema_compliance = {
            'entity_validation': entity_compliance,
            'relation_validation': relation_compliance,
            'entity_compliance': float(entity_compliance['stats']['valid_entities']) / 
                                max(entity_compliance['stats']['total_entities'], 1)
                                if entity_compliance['stats']['total_entities'] > 0 else 0
        }
        
        report = EvaluationReport.generate_report(
            method_name=method_name,
            entity_metrics=entity_metrics,
            relation_metrics=relation_metrics,
            schema_compliance=schema_compliance,
            output_file=str(self.output_dir / "evaluation" / "evaluation_report.json")
        )
        
        EvaluationReport.print_report(report)
        
        return report
    
    def run_full_pipeline(
        self,
        input_file: str,
        method_name: str = "KGEB-Baseline"
    ) -> dict:
        """
        Run the complete extraction and evaluation pipeline.
        
        Args:
            input_file: Path to input document
            method_name: Name of the extraction method
            
        Returns:
            Complete pipeline results
        """
        print("\n" + "="*60)
        print(f"KGEB Pipeline - {method_name}")
        print("="*60)
        print(f"Start time: {datetime.now().isoformat()}")
        
        # Extract entities
        entities, entity_stats, entities_file = self.extract_entities(input_file)
        
        # Extract relations
        relations, relation_stats, relations_file = self.extract_relations(
            input_file,
            entities_file
        )
        
        # Evaluate
        report = self.evaluate(
            entities_file,
            relations_file,
            method_name=method_name
        )
        
        print(f"\nEnd time: {datetime.now().isoformat()}")
        print("="*60)
        
        return {
            'entities': entities,
            'entity_stats': entity_stats,
            'relations': relations,
            'relation_stats': relation_stats,
            'evaluation': report
        }


def main():
    """Main entry point for the pipeline."""
    parser = argparse.ArgumentParser(
        description='Enterprise Knowledge Graph Extraction Benchmark (KGEB)'
    )
    parser.add_argument(
        '--input',
        default='documents.txt',
        help='Input document file'
    )
    parser.add_argument(
        '--output-dir',
        default='output',
        help='Output directory for results'
    )
    parser.add_argument(
        '--data-dir',
        default='.',
        help='Data directory containing input files'
    )
    parser.add_argument(
        '--method',
        default='KGEB-Baseline',
        help='Name of the extraction method'
    )
    parser.add_argument(
        '--entities-schema',
        default='entities.json',
        help='Path to entities schema'
    )
    parser.add_argument(
        '--relations-schema',
        default='relations.json',
        help='Path to relations schema'
    )
    
    args = parser.parse_args()
    
    # Initialize and run pipeline
    pipeline = KGEBPipeline(
        data_dir=args.data_dir,
        output_dir=args.output_dir,
        entities_schema=args.entities_schema,
        relations_schema=args.relations_schema
    )
    
    results = pipeline.run_full_pipeline(
        input_file=args.input,
        method_name=args.method
    )
    
    print(f"\n✓ Pipeline completed successfully")
    print(f"Output saved to: {args.output_dir}")


if __name__ == '__main__':
    main()
