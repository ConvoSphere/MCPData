from __future__ import annotations

from sqlalchemy import inspect
from sqlalchemy.engine import Engine

from .models import ColumnInfo, SchemaSnapshot, TableInfo


class SchemaIntrospector:
	def __init__(self, engine: Engine) -> None:
		self.engine = engine

	def list_tables(self, schema: str | None = None) -> list[TableInfo]:
		inspector = inspect(self.engine)
		tables: list[TableInfo] = []
		for table_name in inspector.get_table_names(schema=schema):
			columns = []
			for col in inspector.get_columns(table_name, schema=schema):
				columns.append(
					ColumnInfo(
						name=str(col.get("name")),
						type=str(col.get("type")),
						nullable=bool(col.get("nullable", True)),
						default=col.get("default"),
						comment=None,
					)
				)
			pk = inspector.get_pk_constraint(table_name, schema=schema)
			pks = pk.get("constrained_columns", []) if pk else []
			fks_raw = inspector.get_foreign_keys(table_name, schema=schema)
			fks = {}
			for fk in fks_raw:
				cols = fk.get("constrained_columns", [])
				referred = fk.get("referred_table")
				for c in cols:
					fks[c] = referred or ""
			tables.append(
				TableInfo(schema_name=schema, name=table_name, columns=columns, primary_key=pks, foreign_keys=fks)
			)
		return tables

	def snapshot(self, schema: str | None = None) -> SchemaSnapshot:
		tables = self.list_tables(schema=schema)
		return SchemaSnapshot(connection=str(self.engine.url), Dialect=self.engine.name, tables=tables)