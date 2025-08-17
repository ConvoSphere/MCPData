# NL → SQL

- Kontextaufbau: Schema- und Ontologie-Snippets via Retriever
- Prompting über litellm (konfigurierbares Modell)
- Validierung: SQL-Parsing (sqlglot), nur-SELECT, LIMIT erzwingen
- Ausführung im Safe-Mode optional (zuerst EXPLAIN)

## Ontologie laden (YAML)

Beispiel `ontologies/customer_sales.yml`:

```yaml
entities:
  - name: customer
    description: Kundenstammdaten
    table: customer
    primary_key: customer_id

dimensions:
  - name: customer_name
    column: customer_name

measures:
  - name: total_revenue
    expression: SUM(order_amount)
```

In Python laden:

```python
from db_semantic_layer.semantic.ontology_loader import load_ontology_from_yaml
onto = load_ontology_from_yaml("ontologies/customer_sales.yml")
```