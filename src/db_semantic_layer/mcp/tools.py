from __future__ import annotations

from typing import Optional
from mcp.server.fastmcp import FastMCP, Tool
from sqlalchemy import text
from ..core.engine_manager import get_global_engine_manager
from ..core.schema_introspect import SchemaIntrospector
from ..core.sql_validator import SQLValidator
from ..semantic.nl2sql import NL2SQL


mcp = FastMCP()


@mcp.tool()
def connect_engine(name: str, url: str) -> str:
	"""Registriert eine neue Verbindung."""
	mgr = get_global_engine_manager()
	mgr.create(name=name, url=url)
	return f"connected:{name}"


@mcp.tool()
def list_connections() -> dict:
	"""Listet alle Verbindungen auf."""
	mgr = get_global_engine_manager()
	return mgr.list()


@mcp.tool()
def inspect_schema(name: Optional[str] = None, schema: Optional[str] = None) -> dict:
	mgr = get_global_engine_manager()
	engine = mgr.get(name)
	ins = SchemaIntrospector(engine)
	return ins.snapshot(schema=schema).model_dump()


@mcp.tool()
def run_sql(sql: str, name: Optional[str] = None, safe_mode: bool = True) -> dict:
	mgr = get_global_engine_manager()
	engine = mgr.get(name)
	validator = SQLValidator(dialect=engine.name)
	validated_sql = validator.validate_readonly(sql) if safe_mode else sql
	with engine.connect() as conn:
		res = conn.execute(text(validated_sql))
		rows = res.fetchall()
		cols = list(res.keys())
	return {"columns": cols, "rows": [list(r) for r in rows], "rowcount": len(rows)}


@mcp.tool()
def semantic_query(question: str, name: Optional[str] = None) -> dict:
	mgr = get_global_engine_manager()
	engine = mgr.get(name)
	# Minimales Schema als Kontext
	ins = SchemaIntrospector(engine)
	tables = ins.list_tables()
	schema_text = "\n".join(
		f"{t.name}: " + ", ".join(c.name for c in t.columns) for t in tables
	)
	nl = NL2SQL(dialect=engine.name)
	sql = nl.generate_sql(question, schema_text)
	return run_sql(sql=sql, name=name, safe_mode=True)