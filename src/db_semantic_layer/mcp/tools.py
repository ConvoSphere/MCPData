from __future__ import annotations

from typing import Any, Dict, List, TypedDict, cast

from mcp.server.fastmcp import FastMCP
from sqlalchemy import text

from ..core.engine_manager import get_global_engine_manager
from ..core.schema_introspect import SchemaIntrospector
from ..core.sql_validator import SQLValidator
from ..semantic.nl2sql import NL2SQL

class SQLResult(TypedDict):
	columns: List[str]
	rows: List[List[Any]]
	rowcount: int

mcp = FastMCP()


@mcp.tool()
def connect_engine(name: str, url: str) -> str:
	"""Registriert eine neue Verbindung."""
	mgr = get_global_engine_manager()
	mgr.create(name=name, url=url)
	return f"connected:{name}"


@mcp.tool()
def list_connections() -> Dict[str, str]:
	"""Listet alle Verbindungen auf."""
	mgr = get_global_engine_manager()
	return mgr.list()


@mcp.tool()
def inspect_schema(name: str | None = None, schema: str | None = None) -> Dict[str, Any]:
	mgr = get_global_engine_manager()
	engine = mgr.get(name)
	ins = SchemaIntrospector(engine)
	# model_dump returns Dict[str, Any]
	return cast(Dict[str, Any], ins.snapshot(schema=schema).model_dump())


@mcp.tool()
def run_sql(sql: str, name: str | None = None, safe_mode: bool = True) -> SQLResult:
	mgr = get_global_engine_manager()
	engine = mgr.get(name)
	validator = SQLValidator(dialect=engine.name)
	validated_sql = validator.validate_readonly(sql) if safe_mode else sql
	with engine.connect() as conn:
		res = conn.execute(text(validated_sql))
		rows = res.fetchall()
		cols = list(res.keys())
	rows_list: List[List[Any]] = [list(r) for r in rows]
	result: SQLResult = {"columns": cols, "rows": rows_list, "rowcount": len(rows_list)}
	return result


@mcp.tool()
def semantic_query(question: str, name: str | None = None) -> SQLResult:
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
	return cast(SQLResult, run_sql(sql=sql, name=name, safe_mode=True))