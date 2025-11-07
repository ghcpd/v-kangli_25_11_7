"""
KGEB schema helpers and validation
"""
import json
from typing import Dict, Any


def load_schema(schema_path: str) -> Dict[str, Any]:
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)
    return schema


def validate_entity(entity_type: str, entity: Dict[str, Any], schema: Dict[str, Any]) -> bool:
    """Check that entity contains only fields defined in the schema, and that all required fields exist.
    For this baseline, required fields are all fields listed in schema for the entity_type.
    """
    if entity_type not in schema:
        return False
    required = set(schema[entity_type])
    keys = set(entity.keys())
    # Check required present
    if not required.issubset(keys):
        return False
    # Check no unknown fields
    if not keys.issubset(required):
        return False
    return True
