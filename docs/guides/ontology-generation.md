# Ontology generation (LLM-assisted)

This guide shows how to bootstrap a semantic ontology (entities, dimensions, measures, synonyms) from your database schema using an LLM via litellm.

## Prerequisites
- Configure a connection (see Guides → Configuring connections)
- Set provider API keys per litellm conventions (e.g., `OPENAI_API_KEY`)
- Optionally set `DBSL_LLM_MODEL` in your `.env`

## CLI

```bash
# Create a named connection
 dbsl connect mydb sqlite:///example.db

# Generate ontology YAML (German prompt), write to file
 dbsl ontology-generate --name mydb --schema main --outfile ontologies/generated.yml --language de

# Include up to N sample rows per table in the prompt
 dbsl ontology-generate --name mydb --samples 3

# Print to stdout (English prompt)
 dbsl ontology-generate --name mydb --language en
```

The command introspects the schema, optionally samples a few rows per table, prompts the LLM, and prints (or writes) YAML. The YAML is validated against the `Ontology` model; warnings are printed if the structure is incomplete.

## Programmatic usage

```python
from db_semantic_layer.core.engine_manager import get_global_engine_manager
from db_semantic_layer.core.schema_introspect import SchemaIntrospector
from db_semantic_layer.semantic.ontology_generation import build_schema_context, generate_ontology_yaml_from_context

mgr = get_global_engine_manager()
engine = mgr.create(name="mem", url="sqlite+pysqlite:///:memory:")
ins = SchemaIntrospector(engine)
snap = ins.snapshot()
ctx = build_schema_context(snap.model_dump())
yaml_text = generate_ontology_yaml_from_context(ctx, language="en")
print(yaml_text)
```

## Notes
- Review the generated YAML before use. Load and validate via `load_ontology_from_yaml` or `Ontology(**yaml.safe_load(...))`.
- For larger schemas, add a retriever step to limit prompt context if needed.