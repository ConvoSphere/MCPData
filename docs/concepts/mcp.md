# Model Context Protocol (MCP)

The server exposes tools over stdio, Unix sockets, and HTTP. Start via CLI: `dbsl mcp-serve --server unix --path /tmp/dbsl.sock` or `--server http`.

Available tools:
- connect_engine, list_connections
- inspect_schema
- run_sql (read-only, safe mode)
- semantic_query