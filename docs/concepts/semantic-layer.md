# Semantic layer

- dbt-like ontology: Entities, Dimensions, Measures, mapping to physical tables/columns.
- Embeddings via litellm (configurable).
- In-memory retriever utility for similarity search.
- NL→SQL currently uses a schema-only context by default; integrating ontology/embeddings is left to custom pipelines.