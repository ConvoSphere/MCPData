# NL → SQL

- Kontextaufbau: Schema- und Ontologie-Snippets via Retriever
- Prompting über litellm (konfigurierbares Modell)
- Validierung: SQL-Parsing (sqlglot), nur-SELECT, LIMIT erzwingen
- Ausführung im Safe-Mode optional (zuerst EXPLAIN)