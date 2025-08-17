# Architektur

Die Architektur gliedert sich in vier Schichten:

1. Core (SQLAlchemy, Registry, Introspektion, SQL-Validierung)
2. Semantik (Ontologie, Embeddings, Retrieval, NL→SQL)
3. MCP (Server, Tools, Ressourcen) über Unix-Sockets und HTTP
4. CLI/API (Bedienung, Automatisierung)

Observability mit OpenTelemetry ist optional aktivierbar.