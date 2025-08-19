# API

Public modules:

- `db_semantic_layer.core`
  - `EngineManager`: create/list/get SQLAlchemy engines and healthcheck
  - `SchemaIntrospector`: list tables and snapshot schema
  - `SQLValidator`: validate SELECT-only and enforce LIMIT
- `db_semantic_layer.semantic`
  - `NL2SQL`: generate SQL from natural language (schema-only context by default)
  - `EmbeddingClient`: create embeddings via litellm
  - `Ontology`, `load_ontology_from_yaml`, and in-memory `InMemoryVectorIndex`
- `db_semantic_layer.mcp`
  - Tools: `connect_engine`, `list_connections`, `inspect_schema`, `run_sql`, `semantic_query`

CLI entrypoint: `dbsl`.
