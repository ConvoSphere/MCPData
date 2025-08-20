# DB Semantic Layer

Lightweight abstraction and semantic layer for SQL databases via SQLAlchemy. Provides NL→SQL with an LLM (litellm) and exposes tools over MCP (stdio/Unix socket/HTTP). Strict read-only execution with SQL validation and automatic LIMIT. OpenTelemetry instrumentation is optional.

- Supported dialects: any SQLAlchemy dialect. Tested with SQLite; optional extras available for PostgreSQL, Trino, and MySQL.

Quickstart:

```bash
pip install -e .
dbsl --help
dbsl ontology-generate --help
```