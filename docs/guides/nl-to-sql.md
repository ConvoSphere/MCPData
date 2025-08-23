# NL → SQL

- Context: by default, NL→SQL uses schema snippets (table/column names). Ontology/embeddings are available in the library, but not wired into the default CLI flow.
- Prompting via litellm (configurable model in settings)
- Validation: SQL parsing (sqlglot), SELECT‑only, enforced LIMIT
- Execution: safe mode validates before execution; no EXPLAIN phase is implemented

## Via MCP tool

```bash
# Start MCP server (stdio)
dbsl mcp-serve --server stdio
```

Client calls `semantic_query(question, name?)` and receives `{columns, rows, rowcount}`. Example question: "Top 5 products by price".

## Programmatic usage

```python
from db_semantic_layer.semantic.nl2sql import NL2SQL
from db_semantic_layer.semantic.ontology_generation import build_schema_context
from db_semantic_layer.core.schema_introspect import SchemaIntrospector
from db_semantic_layer.core.engine_manager import get_global_engine_manager

mgr = get_global_engine_manager()
engine = mgr.get("mydb")
ins = SchemaIntrospector(engine)
ctx = build_schema_context(ins.snapshot().model_dump())

nl = NL2SQL(dialect=engine.name)
sql = nl.generate_sql("Top 5 products by price", ctx)
# sql is validated SELECT with LIMIT
```