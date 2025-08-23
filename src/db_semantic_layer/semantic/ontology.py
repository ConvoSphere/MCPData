from __future__ import annotations

from pydantic import BaseModel, Field


class Entity(BaseModel):
	name: str
	description: str | None = None
	table: str | None = None
	primary_key: str | None = None


class Measure(BaseModel):
	name: str
	expression: str
	description: str | None = None


class Dimension(BaseModel):
	name: str
	column: str
	description: str | None = None


class Ontology(BaseModel):
	entities: list[Entity] = Field(default_factory=list)
	dimensions: list[Dimension] = Field(default_factory=list)
	measures: list[Measure] = Field(default_factory=list)
	synonyms: dict[str, list[str]] = Field(default_factory=dict)

	def find_entity(self, name: str) -> Entity | None:
		for e in self.entities:
			if e.name == name:
				return e
		return None