"""
Main Pipeline Script for KGEB
Orchestrates entity extraction, relation extraction, and evaluation.
"""

import argparse
import json
import sys
from pathlib import Path

from entity_extraction import extract_entities
from relation_extraction import extract_relations
from evaluator import evaluate_extraction


def main():
    """Main pipeline execution."""
    parser = argparse.ArgumentParser(
        description="Enterprise Knowledge Graph Extraction Benchmark (KGEB) Pipeline"
    )
    parser.add_argument(
        "--documents", 
        type=str, 
        default="documents.txt",
        help="Path to documents.txt"
    )
    parser.add_argument(
        "--entities-schema",
        type=str,
        default="entities.json",
        help="Path to entities.json"
    )
    parser.add_argument(
        "--relations-schema",
        type=str,
        default="relations.json",
        help="Path to relations.json"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=".",
        help="Output directory for results"
    )
    parser.add_argument(
        "--method-name",
        type=str,
        default="Baseline Method",
        help="Name of the extraction method"
    )
    parser.add_argument(
        "--skip-extraction",
        action="store_true",
        help="Skip extraction and only run evaluation (requires existing outputs)"
    )
    
    args = parser.parse_args()
    
    # Set output paths
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    entities_output = output_dir / "entities_output.json"
    relations_output = output_dir / "relations_output.json"
    evaluation_output = output_dir / "evaluation_report.json"
    
    print("=" * 60)
    print("Enterprise Knowledge Graph Extraction Benchmark (KGEB)")
    print("=" * 60)
    print()
    
    # Step 1: Entity Extraction
    if not args.skip_extraction:
        print("Step 1: Extracting entities...")
        try:
            extract_entities(
                args.documents,
                args.entities_schema,
                str(entities_output)
            )
            print("✓ Entity extraction completed\n")
        except Exception as e:
            print(f"✗ Entity extraction failed: {e}")
            sys.exit(1)
    else:
        if not entities_output.exists():
            print(f"✗ Error: {entities_output} not found. Cannot skip extraction.")
            sys.exit(1)
        print("Skipping entity extraction (using existing output)\n")
    
    # Step 2: Relation Extraction
    if not args.skip_extraction:
        print("Step 2: Extracting relations...")
        try:
            extract_relations(
                args.documents,
                args.relations_schema,
                str(entities_output),
                str(relations_output)
            )
            print("✓ Relation extraction completed\n")
        except Exception as e:
            print(f"✗ Relation extraction failed: {e}")
            sys.exit(1)
    else:
        if not relations_output.exists():
            print(f"✗ Error: {relations_output} not found. Cannot skip extraction.")
            sys.exit(1)
        print("Skipping relation extraction (using existing output)\n")
    
    # Step 3: Evaluation
    print("Step 3: Evaluating results...")
    try:
        evaluate_extraction(
            str(entities_output),
            str(relations_output),
            args.entities_schema,
            args.relations_schema,
            str(evaluation_output),
            args.method_name
        )
        print("✓ Evaluation completed\n")
    except Exception as e:
        print(f"✗ Evaluation failed: {e}")
        sys.exit(1)
    
    print("=" * 60)
    print("Pipeline execution completed successfully!")
    print("=" * 60)
    print(f"\nResults saved to:")
    print(f"  - Entities: {entities_output}")
    print(f"  - Relations: {relations_output}")
    print(f"  - Evaluation: {evaluation_output}")


if __name__ == "__main__":
    main()

