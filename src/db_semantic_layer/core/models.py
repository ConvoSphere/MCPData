from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ConnectionConfig(BaseModel):
	name: str
	url: str
	dialect: str | None = None


class ColumnInfo(BaseModel):
	name: str
	type: str
	nullable: bool
	default: Any | None = None
	comment: str | None = None


class TableInfo(BaseModel):
	schema: str | None
	name: str
	columns: list[ColumnInfo] = Field(default_factory=list)
	primary_key: list[str] = Field(default_factory=list)
	foreign_keys: dict[str, str] = Field(default_factory=dict)
	comment: str | None = None


class SchemaSnapshot(BaseModel):
	connection: str
	Dialect: str | None = None
	tables: list[TableInfo] = Field(default_factory=list)


class QueryResult(BaseModel):
	columns: list[str]
	rows: list[list[Any]]
	rowcount: int
	executed_sql: str


class SemanticEntity(BaseModel):
	name: str
	description: str | None = None
	table: str | None = None
	primary_key: str | None = None


class SemanticMeasure(BaseModel):
	name: str
	expression: str
	description: str | None = None


class SemanticDimension(BaseModel):
	name: str
	column: str
	description: str | None = None


class OntologyModel(BaseModel):
	entities: list[SemanticEntity] = Field(default_factory=list)
	dimensions: list[SemanticDimension] = Field(default_factory=list)
	measures: list[SemanticMeasure] = Field(default_factory=list)
	synonyms: dict[str, list[str]] = Field(default_factory=dict)