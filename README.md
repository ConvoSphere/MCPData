# DB Semantic Layer

A lightweight abstraction and semantic layer for SQL databases using SQLAlchemy. It provides NL→SQL via an LLM (litellm) and exposes safe, read‑only query tools over the Model Context Protocol (MCP) for agent integrations.

- Supported dialects: any SQLAlchemy dialect. Tested with SQLite; optional extras for PostgreSQL, Trino, and MySQL
- Safety: SELECT‑only validation with automatic LIMIT injection (sqlglot)
- Transports: MCP over stdio, Unix socket, and HTTP
- Ontology: simple dbt‑like model (Entities, Dimensions, Measures) and an LLM‑assisted generator

## Install

- Local dev (editable):

```bash
pip install -e ".[dev]"
# or with extras
pip install -e ".[postgres,trino,mysql,telemetry,dev]"
```

- Runtime (no dev tools):

```bash
pip install .
# or with extras: pip install ".[postgres]" etc.
```

Python >= 3.10 is required. Set provider API keys per litellm conventions (e.g., `OPENAI_API_KEY`).

## Quickstart (CLI)

```bash
# Create a named connection
dbsl connect mydb "sqlite:///example.db"

# List and inspect
dbsl connections
dbsl schema --name mydb --schema main

# Run a safe (validated) SQL query
dbsl sql --name mydb "select 1"
```

Notes:
- The first created connection becomes the default. You can override the default via `DBSL_DEFAULT_CONNECTION`.
- Validation enforces SELECT‑only and injects a LIMIT if missing.

## MCP server

Start the MCP server to expose tools to agents:

```bash
# stdio (for MCP clients that spawn the process)
dbsl mcp-serve --server stdio

# Unix socket (default path if omitted)
dbsl mcp-serve --server unix --path /tmp/dbsl.sock

# HTTP
dbsl mcp-serve --server http --host 127.0.0.1 --port 8081
```

Available tools:
- `connect_engine(name, url)` and `list_connections()`
- `inspect_schema(name?, schema?)`
- `run_sql(sql, name?, safe_mode=True)`
- `semantic_query(question, name?)` → generates SQL via LLM, validates, then executes

## Ontology generation (LLM‑assisted)

```bash
dbsl ontology-generate --name mydb --schema main --outfile ontologies/generated.yml --language en
# include sample rows in the prompt
dbsl ontology-generate --name mydb --samples 3
```

You can load YAML programmatically via `db_semantic_layer.semantic.ontology_loader.load_ontology_from_yaml`.

## Settings (.env)

Settings are read with prefix `DBSL_` (via pydantic‑settings):
- `DBSL_LLM_MODEL` (default: `gpt-4o-mini`)
- `DBSL_EMBEDDING_MODEL` (default: `text-embedding-3-small`)
- `DBSL_TELEMETRY_ENABLED` (default: `false`)
- `DBSL_OTEL_ENDPOINT` (e.g., `http://localhost:4317` for OTLP gRPC)
- `DBSL_DEFAULT_CONNECTION` (default connection name)

## Development

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pre-commit install
pytest -q

# Docs (MkDocs Material)
mkdocs serve
```

## License

MIT — see `LICENSE`.