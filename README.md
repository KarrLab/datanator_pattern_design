# Repo for storing and validating $jsonSchema of documents stored in MongoDB

## Introduction
Background on JSON Schema [http://json-schema.org/](http://json-schema.org/).

Note files in `components` directory cannot be used directly for [$jsonSchema](https://docs.mongodb.com/master/reference/operator/query/jsonSchema/) because MongoDB omits `$ref`. Use files in `compiled` directory where `$ref` is resolved using `jsonschema`.

## Instructions

```
pip install jsonschema
jsonschema -i sample_files/taxon/taxon_incorrect.json components/taxon.json
jsonschema -i sample_files/taxon/taxon_correct.json components/taxon.json
```