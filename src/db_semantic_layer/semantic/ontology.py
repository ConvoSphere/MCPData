from __future__ import annotations

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class Entity(BaseModel):
	name: str
	description: Optional[str] = None
	table: Optional[str] = None
	primary_key: Optional[str] = None


class Measure(BaseModel):
	name: str
	expression: str
	description: Optional[str] = None


class Dimension(BaseModel):
	name: str
	column: str
	description: Optional[str] = None


class Ontology(BaseModel):
	entities: List[Entity] = Field(default_factory=list)
	dimensions: List[Dimension] = Field(default_factory=list)
	measures: List[Measure] = Field(default_factory=list)
	synonyms: Dict[str, List[str]] = Field(default_factory=dict)

	def find_entity(self, name: str) -> Optional[Entity]:
		for e in self.entities:
			if e.name == name:
				return e
		return None