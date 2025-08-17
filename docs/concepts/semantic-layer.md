# Semantische Schicht

- DBT-ähnliche Ontologie: Entities, Dimensions, Measures, Mappings auf physische Tabellen/Spalten.
- Embeddings über litellm konfigurierbar (API-gestützt), alternativ lokal.
- Retriever priorisiert relevante Schemafragmente für NL→SQL.
- NL→SQL orchestriert Prompting, Validierung und Safe-Mode-Ausführung.