import os
import json
import jsonschema


def is_valid(project_description):
    schema_file_path = f'{os.path.dirname(__file__)}/project_schema.json'
    print(f'opening schema file {schema_file_path}')
    with open(schema_file_path) as schema_file:
        schema = json.load(schema_file)
    try:
        jsonschema.validate(project_description, schema)
        return True
    except jsonschema.ValidationError as e:
        print(f'message: {e.message}')
        print(f'path: {e.path[0]}')
        return False
