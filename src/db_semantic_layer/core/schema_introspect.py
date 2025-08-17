from __future__ import annotations

from typing import List, Optional
from sqlalchemy import inspect
from sqlalchemy.engine import Engine
from .models import TableInfo, ColumnInfo, SchemaSnapshot


class SchemaIntrospector:
	def __init__(self, engine: Engine) -> None:
		self.engine = engine

	def list_tables(self, schema: Optional[str] = None) -> List[TableInfo]:
		inspector = inspect(self.engine)
		tables: List[TableInfo] = []
		for table_name in inspector.get_table_names(schema=schema):
			columns = []
			for col in inspector.get_columns(table_name, schema=schema):
				columns.append(
					ColumnInfo(
						name=col.get("name"),
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
				TableInfo(schema=schema, name=table_name, columns=columns, primary_key=pks, foreign_keys=fks)
			)
		return tables

	def snapshot(self, schema: Optional[str] = None) -> SchemaSnapshot:
		tables = self.list_tables(schema=schema)
		return SchemaSnapshot(connection=str(self.engine.url), Dialect=self.engine.name, tables=tables)