# Model Context Protocol (MCP)

The server exposes tools over stdio, Unix sockets, and HTTP. Start via the CLI:

```bash
# stdio (for MCP clients that spawn the process)
dbsl mcp-serve --server stdio

# Unix socket
dbsl mcp-serve --server unix --path /tmp/dbsl.sock

# HTTP
dbsl mcp-serve --server http --host 127.0.0.1 --port 8081
```

Available tools:
- `connect_engine(name, url)` and `list_connections()`
- `inspect_schema(name?, schema?)` → returns a JSON schema snapshot
- `run_sql(sql, name?, safe_mode=True)` → validates SELECT‑only and enforces LIMIT in safe mode
- `semantic_query(question, name?)` → generates SQL via LLM using a schema‑only context, validates, executes, and returns `{columns, rows, rowcount}`