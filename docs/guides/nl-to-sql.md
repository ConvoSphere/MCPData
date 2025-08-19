# NL → SQL

- Context: by default, NL→SQL uses schema snippets (table/column names). Ontology/embeddings are available in the library, but not wired into the default CLI flow.
- Prompting via litellm (configurable model in settings)
- Validation: SQL parsing (sqlglot), SELECT-only, enforced LIMIT
- Execution: safe mode enforces read-only and validation; no EXPLAIN phase is implemented.

## Load ontology (YAML)

Example `ontologies/customer_sales.yml`:

```yaml
entities:
  - name: customer
    description: Customer master data
    table: customer
    primary_key: customer_id

dimensions:
  - name: customer_name
    column: customer_name

measures:
  - name: total_revenue
    expression: SUM(order_amount)
```

In Python:

```python
from db_semantic_layer.semantic.ontology_loader import load_ontology_from_yaml
onto = load_ontology_from_yaml("ontologies/customer_sales.yml")
```