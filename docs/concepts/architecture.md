# Architecture

Layers:

1. Core (SQLAlchemy, engine registry, schema introspection, SQL validation)
2. Semantics (ontology, embeddings, retriever, NL→SQL)
3. MCP (server, tools) over stdio, Unix sockets, and HTTP
4. CLI/API (operations, automation)

Observability with OpenTelemetry can be enabled optionally (requires extras).