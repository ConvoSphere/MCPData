# DB Semantic Layer

A lightweight abstraction and semantic layer for relational databases via SQLAlchemy. It provides NL→SQL via an LLM (litellm) and exposes tools through the Model Context Protocol (MCP) for AI agents.

- Supported dialects: any SQLAlchemy dialect. Tested with SQLite; optional extras for PostgreSQL, Trino, and MySQL.
- Security: strict read-only mode with SQL validation and automatic LIMIT.
- Transports: MCP over stdio, Unix socket, and HTTP.
- Ontology: simple, dbt-like model (Entities, Dimensions, Measures) available for custom pipelines; not wired into the default NL→SQL flow.

Get started in Guides or run `dbsl --help`.