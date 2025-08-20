from __future__ import annotations

from db_semantic_layer.core.engine_manager import get_global_engine_manager
from db_semantic_layer.mcp.tools import semantic_query


def test_semantic_query_with_mocked_llm(monkeypatch):
	mgr = get_global_engine_manager()
	mgr.create(name="mem2", url="sqlite+pysqlite:///:memory:")
	engine = mgr.get("mem2")
	with engine.begin() as conn:
		conn.exec_driver_sql(
			"""
			CREATE TABLE products (
				product_id INTEGER PRIMARY KEY,
				name TEXT,
				price REAL
			)
			"""
		)
		conn.exec_driver_sql(
			"""
			INSERT INTO products (product_id, name, price) VALUES (1, 'A', 10.0), (2, 'B', 20.0)
			"""
		)

	# Mock the completion function used by NL2SQL to return a simple valid SQL
	def fake_completion(model, messages):  # type: ignore
		return {
			"choices": [
				{
					"message": {
						"content": "SELECT name, price FROM products ORDER BY price DESC LIMIT 5"
					}
				}
			]
		}

	monkeypatch.setattr("db_semantic_layer.semantic.nl2sql.completion", fake_completion)

	res = semantic_query(question="Top 5 products by price", name="mem2")
	assert "columns" in res and "rows" in res
	assert res["rows"][0][0] == "B"  # highest price first