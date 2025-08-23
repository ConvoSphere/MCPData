# DB Semantic Layer

A lightweight abstraction and semantic layer for relational databases via SQLAlchemy. It provides NL→SQL via an LLM (litellm) and exposes tools through the Model Context Protocol (MCP) for AI agents.

- Supported dialects: any SQLAlchemy dialect. Tested with SQLite; optional extras for PostgreSQL, Trino, and MySQL
- Security: strict read‑only mode with SQL validation and automatic LIMIT
- Transports: MCP over stdio, Unix socket, and HTTP
- Ontology: dbt‑like model (Entities, Dimensions, Measures) and an LLM‑assisted generator

Quickstart:

```bash
dbsl connect mydb "sqlite:///example.db"
dbsl schema --name mydb --schema main
dbsl sql --name mydb "select 1"
```

Continue in Guides or run `dbsl --help`.