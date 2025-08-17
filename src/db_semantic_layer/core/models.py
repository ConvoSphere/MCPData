from __future__ import annotations

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class ConnectionConfig(BaseModel):
	name: str
	url: str
	dialect: Optional[str] = None


class ColumnInfo(BaseModel):
	name: str
	type: str
	nullable: bool
	default: Optional[Any] = None
	comment: Optional[str] = None


class TableInfo(BaseModel):
	schema: Optional[str]
	name: str
	columns: List[ColumnInfo] = Field(default_factory=list)
	primary_key: List[str] = Field(default_factory=list)
	foreign_keys: Dict[str, str] = Field(default_factory=dict)
	comment: Optional[str] = None


class SchemaSnapshot(BaseModel):
	connection: str
	Dialect: Optional[str] = None
	tables: List[TableInfo] = Field(default_factory=list)


class QueryResult(BaseModel):
	columns: List[str]
	rows: List[List[Any]]
	rowcount: int
	executed_sql: str


class SemanticEntity(BaseModel):
	name: str
	description: Optional[str] = None
	table: Optional[str] = None
	primary_key: Optional[str] = None


class SemanticMeasure(BaseModel):
	name: str
	expression: str
	description: Optional[str] = None


class SemanticDimension(BaseModel):
	name: str
	column: str
	description: Optional[str] = None


class OntologyModel(BaseModel):
	entities: List[SemanticEntity] = Field(default_factory=list)
	dimensions: List[SemanticDimension] = Field(default_factory=list)
	measures: List[SemanticMeasure] = Field(default_factory=list)
	synonyms: Dict[str, List[str]] = Field(default_factory=dict)