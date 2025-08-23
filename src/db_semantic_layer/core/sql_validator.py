from __future__ import annotations

import sqlglot
from sqlglot import exp


class SQLValidationError(ValueError):
	pass


class SQLValidator:
	def __init__(self, dialect: str | None = None, enforce_limit: int = 1000) -> None:
		self.dialect = dialect
		self.enforce_limit = enforce_limit

	def validate_readonly(self, sql: str) -> str:
		try:
			tree = sqlglot.parse_one(sql, read=self.dialect)
		except Exception as exc:  # pragma: no cover
			raise SQLValidationError(f"SQL konnte nicht geparst werden: {exc}") from exc
		if not isinstance(tree, exp.Select):
			raise SQLValidationError("Nur SELECT-Abfragen sind erlaubt.")
		# LIMIT erzwingen, falls nicht vorhanden
		if not tree.args.get("limit") and self.enforce_limit:
			limit_expr = exp.Limit(this=exp.Literal.number(self.enforce_limit))
			tree.set("limit", limit_expr)
		return str(tree.sql(dialect=self.dialect))