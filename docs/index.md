# DB Semantic Layer

Eine Abstraktions- und semantische Schicht für relationale Datenbanken über SQLAlchemy. Bietet eine NL→SQL-Funktionalität via LLM (litellm) und stellt Funktionen über das Model Context Protocol (MCP) für AI-Agenten bereit.

- Unterstützte Dialekte (v0.1): PostgreSQL, Trino, MySQL
- Sicherheit: Strikter Read-Only-Modus und SQL-Validierung
- Transports: MCP über Unix-Socket und HTTP
- Ontologie: DBT-ähnliches Modell (Entities, Dimensions, Measures)

Los geht's unter "Anleitungen" oder starte die CLI mit `dbsl --help`.