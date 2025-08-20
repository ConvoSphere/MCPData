from __future__ import annotations

import json
from typer.testing import CliRunner
from db_semantic_layer.cli.app import app
from db_semantic_layer.core.engine_manager import get_global_engine_manager


runner = CliRunner()


def test_ontology_generate_with_sqlite_monkeypatch(monkeypatch):
	# Setup: create in-memory sqlite engine
	mgr = get_global_engine_manager()
	mgr.create(name="mem", url="sqlite+pysqlite:///:memory:")
	# Create simple tables
	engine = mgr.get("mem")
	with engine.begin() as conn:
		conn.exec_driver_sql(
			"""
			CREATE TABLE customers (
				customer_id INTEGER PRIMARY KEY,
				name TEXT
			)
			"""
		)
		conn.exec_driver_sql(
			"""
			CREATE TABLE orders (
				order_id INTEGER PRIMARY KEY,
				customer_id INTEGER,
				amount REAL
			)
			"""
		)

	# Monkeypatch litellm.completion to return a deterministic YAML
	def fake_completion(model, messages):  # type: ignore
		return {
			"choices": [
				{
					"message": {
						"content": (
							"entities:\n"
							"  - name: customer\n"
							"    table: customers\n"
							"    primary_key: customer_id\n"
							"dimensions:\n"
							"  - name: customer_name\n"
							"    column: name\n"
							"measures:\n"
							"  - name: total_amount\n"
							"    expression: SUM(amount)\n"
							"synonyms: {}\n"
						)
					}
				}
			]
		}

	monkeypatch.setitem(__import__("sys").modules, "litellm", type("M", (), {"completion": staticmethod(fake_completion)})())

	# Run CLI: output to stdout
	result = runner.invoke(app, ["ontology-generate", "--name", "mem", "--language", "de"])  # type: ignore
	assert result.exit_code == 0, result.output
	text = result.output.strip()
	assert "entities:" in text
	assert "dimensions:" in text
	assert "measures:" in text

