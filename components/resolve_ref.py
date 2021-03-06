"""
Derived from https://jsonldschema.readthedocs.io/en/latest/_modules/compile_schema.html
"""
import json
from copy import deepcopy as copy


def resolve_reference(schema_url):
    """ Load and decode the schema from a given URL

    :param schema_url: the URL to the schema
    :return: an exception or a decoded json schema as a dictionary
    """
    try:
        with open(schema_url) as f:
            return json.load(f)
    except Exception as e:
        return e

def resolve_schema_references(schema, loaded_schemas, schema_url=None, refs=None):
    """ Resolves and replaces json-schema $refs with the appropriate dict.
    Recursively walks the given schema dict, converting every instance
    of $ref in a 'properties' structure with a resolved dict.
    This modifies the input schema and also returns it.

    :param schema: the schema dict
    :param loaded_schemas: a recursive dictionary that stores the path of
        already loaded schemas to prevent circularity issues
    :param refs: a dict of <string, dict> which forms a store of referenced schema
    :param schema_url: the URL of the schema
    :return: schema
    """
    if schema_url:
        return _resolve_schema_references(schema,
                                          loaded_schemas,
                                          '#')
    else:
        return _resolve_schema_references(schema,
                                          loaded_schemas,
                                          '#')

def _resolve_schema_references(schema, loaded_schemas, object_path):
    """ Iterate over the json until it find a $ref and replace it with the loaded object or a
    reference to an already loaded object

    :param schema: the schema or portion of schema to process
    :param loaded_schemas: a dictionary of a already loaded schemas (prevent recursion issues)
    :param object_path: a string containing the path of the current level inside the document
    :return schema: the updated schema
    """
    if SchemaKey.ref in schema:
        if schema['$ref'][0] != '#':
            reference_path = schema.pop(SchemaKey.ref, None)
            if reference_path not in loaded_schemas:
                with open(reference_path) as f:
                    x = json.load(f)
                loaded_schemas[reference_path] = x
                schema.update(x)
                return (_resolve_schema_references(schema, loaded_schemas,
                                                              object_path))

            else:
                res = loaded_schemas[reference_path]
                schema.update(res)

    if SchemaKey._type in schema: # remove "type" in compiled version
        schema.pop(SchemaKey._type)

    if SchemaKey.properties in schema:
        for k, val in schema[SchemaKey.properties].items():
            current_path = object_path + '/properties/'+k
            schema[SchemaKey.properties][k] = (_resolve_schema_references(val,
                                                                           loaded_schemas,
                                                                           current_path))

    if SchemaKey.definitions in schema:
        for k, val in schema[SchemaKey.definitions].items():
            current_path = object_path + '/definitions/' + k
            schema[SchemaKey.definitions][k] = (
                                                _resolve_schema_references(val,
                                                                           loaded_schemas,
                                                                           current_path))

    for pattern in SchemaKey.sub_patterns:
        i = 0
        if pattern in schema:
            for val in schema[pattern]:
                iterator = str(copy(i))
                current_path = object_path + '/' + pattern + '/' + iterator
                schema[pattern][i] = (_resolve_schema_references(val,
                                                                loaded_schemas,
                                                                current_path))
                i += 1

    if SchemaKey.items in schema:
        current_path = object_path + '/items'
        schema[SchemaKey.items] = (_resolve_schema_references(schema[SchemaKey.items],
                                                            loaded_schemas,
                                                            current_path))

    return (schema)


class SchemaKey:
    ref = "$ref"
    items = "items"
    properties = "properties"
    definitions = 'definitions'
    pattern_properties = "patternProperties"
    _type = "type"
    sub_patterns = ['anyOf', 'oneOf', 'allOf']


def main():
    url = "taxon.json"
    schema = resolve_reference(url)
    resolved = resolve_schema_references(schema, {})
    with open("../compiled/{}_compiled.json".format(url.split(".")[0]), "w+") as f:
        json.dump(resolved, f, indent=4)


from pathlib import Path
def iterate_dir():
    pathlist = Path("./").glob('**/*.json')
    for path in pathlist:
        # because path is object not string
        url = str(path)
        schema = resolve_reference(url)
        resolved = resolve_schema_references(schema, {})
        with open("../compiled/{}_compiled.json".format(url.split(".")[0]), "w+") as f:
            json.dump(resolved, f, indent=4)

if __name__ == "__main__":
    iterate_dir()