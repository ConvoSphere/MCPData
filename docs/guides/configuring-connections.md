# Configuring connections

Configure connections via the CLI.

Example URLs (SQLAlchemy):
- PostgreSQL: `postgresql+psycopg://user:pass@host:5432/db` (requires optional dependency)
- Trino: `trino://user@host:8080/catalog/schema` (requires `sqlalchemy-trino`)
- MySQL: `mysql+pymysql://user:pass@host:3306/db` (requires optional dependency)

Examples:

```bash
dbsl connect mypg "postgresql+psycopg://user:pass@host:5432/db"
dbsl connections
dbsl schema --name mypg --schema public
dbsl sql --name mypg "select 1"
```

Notes:
- Install database drivers via extras, e.g., `pip install -e ".[postgres]"`, `.[trino]`, `.[mysql]`.
- The first created connection becomes the default. Override with `--name` per command, or set `DBSL_DEFAULT_CONNECTION` in `.env` to pick a default name when multiple connections are present.
- litellm requires provider credentials (e.g., `OPENAI_API_KEY`) when using LLM features.