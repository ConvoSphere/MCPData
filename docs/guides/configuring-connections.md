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