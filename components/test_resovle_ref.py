import unittest
import resolve_ref
import json


class TestResolve(unittest.TestCase):

    def test_resolve(self):
        url = "./entity.json"
        schema = resolve_ref.resolve_reference(url)
        result_0 = resolve_ref.resolve_schema_references(schema, {})
        exp = {
                "bsonType": "object",
                "type": "object",
                "required": [
                    "type"
                ],
                "properties": {
                    "type": {
                        "bsonType": "string",
                        "type": "string",
                        "enum": [
                            "metabolite",
                            "protein",
                            "reaction",
                            "RNA"
                        ]
                    },
                    "name": {
                        "bsonType": "string",
                        "type": "string",
                        "description": "Name of protein, RNA, etc."
                    },
                    "synonyms": {
                        "bsonType": "array",
                        "type": "array",
                        "items": {
                            "bsonType": "string",
                            "type": "string"
                        }
                    },
                    "identifiers": {
                        "bsonType": "array",
                        "type": "array",
                        "items": {
                            "bsonType": "object",
                            "type": "object",
                            "required": [
                                "namespace",
                                "value"
                            ],
                            "properties": {
                                "namespace": {
                                    "bsonType": "string",
                                    "type": "string",
                                    "description": "name of the identifier"
                                },
                                "value": {
                                    "bsonType": "string",
                                    "type": "string",
                                    "description": "id"
                                }
                            }
                        }
                    },
                    "related": {
                        "bsonType": "array",
                        "type": "array",
                        "items": {
                            "bsonType": "object",
                            "type": "object",
                            "required": [
                                "namespace",
                                "value"
                            ],
                            "properties": {
                                "namespace": {
                                    "bsonType": "string",
                                    "type": "string",
                                    "description": "name of the identifier"
                                },
                                "value": {
                                    "bsonType": "string",
                                    "type": "string",
                                    "description": "id"
                                }
                            }
                        }
                    }
                }
            }
        self.assertEqual(result_0, exp)