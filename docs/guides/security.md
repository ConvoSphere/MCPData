# Security

- Strict read‑only: only SELECT is allowed (validated by `SQLValidator`)
- Automatic LIMIT injection when missing (prevents unbounded scans)
- Safe execution paths:
  - CLI `dbsl sql` validates before running
  - MCP `run_sql(..., safe_mode=True)` validates before running (default)
  - MCP `semantic_query` generates SQL via LLM, then validates and executes
- Not implemented: timeouts, EXPLAIN/estimates, access control by allowed schemas/tables, row‑level security
- Telemetry: optional OpenTelemetry tracing can be enabled via `DBSL_TELEMETRY_ENABLED=true` and `DBSL_OTEL_ENDPOINT` (OTLP gRPC)