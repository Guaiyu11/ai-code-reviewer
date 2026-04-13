#!/usr/bin/env python3
"""
JSON Schema Validator - Validate JSON files against JSON Schema.
Usage: python json-schema-validator.py <json_file> [--schema SCHEMA_FILE]
"""

import sys
import os
import json

def validate_json(data, schema, path=''):
    """Validate JSON data against a simple schema."""
    errors = []
    
    if 'type' in schema:
        expected_type = schema['type']
        if expected_type == 'object' and not isinstance(data, dict):
            errors.append(f"{path}: expected object, got {type(data).__name__}")
            return errors
        elif expected_type == 'array' and not isinstance(data, list):
            errors.append(f"{path}: expected array, got {type(data).__name__}")
            return errors
        elif expected_type == 'string' and not isinstance(data, str):
            errors.append(f"{path}: expected string, got {type(data).__name__}")
            return errors
        elif expected_type == 'number' and not isinstance(data, (int, float)):
            errors.append(f"{path}: expected number, got {type(data).__name__}")
            return errors
        elif expected_type == 'integer' and not isinstance(data, int):
            errors.append(f"{path}: expected integer, got {type(data).__name__}")
            return errors
        elif expected_type == 'boolean' and not isinstance(data, bool):
            errors.append(f"{path}: expected boolean, got {type(data).__name__}")
            return errors
    
    # Object validation
    if isinstance(data, dict):
        # Required properties
        if 'required' in schema:
            for prop in schema['required']:
                if prop not in data:
                    errors.append(f"{path}.{prop}: required property missing")
        
        # Property validations
        if 'properties' in schema:
            for prop, prop_schema in schema['properties'].items():
                if prop in data:
                    prop_errors = validate_json(data[prop], prop_schema, f"{path}.{prop}")
                    errors.extend(prop_errors)
    
    # Array validation
    if isinstance(data, list) and 'items' in schema:
        for i, item in enumerate(data):
            item_errors = validate_json(item, schema['items'], f"{path}[{i}]")
            errors.extend(item_errors)
    
    # Enum validation
    if 'enum' in schema and data not in schema['enum']:
        errors.append(f"{path}: value must be one of {schema['enum']}")
    
    # String constraints
    if isinstance(data, str) and 'minLength' in schema:
        if len(data) < schema['minLength']:
            errors.append(f"{path}: string too short (min {schema['minLength']}, got {len(data)})")
    
    if isinstance(data, str) and 'maxLength' in schema:
        if len(data) > schema['maxLength']:
            errors.append(f"{path}: string too long (max {schema['maxLength']}, got {len(data)})")
    
    if isinstance(data, str) and 'pattern' in schema:
        import re
        if not re.match(schema['pattern'], data):
            errors.append(f"{path}: does not match pattern {schema['pattern']}")
    
    # Number constraints
    if isinstance(data, (int, float)):
        if 'minimum' in schema and data < schema['minimum']:
            errors.append(f"{path}: value below minimum ({schema['minimum']})")
        if 'maximum' in schema and data > schema['maximum']:
            errors.append(f"{path}: value above maximum ({schema['maximum']})")
    
    return errors


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python json-schema-validator.py <json_file> [--schema SCHEMA_FILE]")
        print("\nExample schema format:")
        print('  {"type": "object", "required": ["name"], "properties": {"name": {"type": "string"}}}')
        sys.exit(1)
    
    json_file = sys.argv[1]
    schema_file = None
    
    for i, arg in enumerate(sys.argv):
        if arg == '--schema' and i + 1 < len(sys.argv):
            schema_file = sys.argv[i + 1]
    
    if not os.path.exists(json_file):
        print(f"Error: File not found: {json_file}")
        sys.exit(1)
    
    # Load JSON
    with open(json_file, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"JSON Parse Error: {e}")
            sys.exit(1)
    
    if schema_file:
        if not os.path.exists(schema_file):
            print(f"Error: Schema file not found: {schema_file}")
            sys.exit(1)
        
        with open(schema_file, 'r') as f:
            try:
                schema = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Schema Parse Error: {e}")
                sys.exit(1)
        
        print(f"=== Validating {json_file} against {schema_file} ===\n")
        errors = validate_json(data, schema)
        
        if not errors:
            print("Validation PASSED")
        else:
            print(f"Validation FAILED ({len(errors)} errors):")
            for err in errors:
                print(f"  - {err}")
    else:
        # Just pretty-print
        print(json.dumps(data, indent=2, ensure_ascii=False)[:2000])
