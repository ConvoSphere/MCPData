# DB Semantic Layer

Abstraktions- und semantische Schicht für SQL-Datenbanken (PostgreSQL, Trino, MySQL) über SQLAlchemy, NL→SQL via LLM (litellm), und Bereitstellung über MCP (Sockets/HTTP). Strikte Sicherheit (Read-Only, SQL-Validierung).

Quickstart:

```bash
pip install -e .
dbsl --help
```