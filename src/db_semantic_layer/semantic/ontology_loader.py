from __future__ import annotations

from typing import Any
import yaml
from .ontology import Ontology, Entity, Dimension, Measure


def load_ontology_from_yaml(path: str) -> Ontology:
	with open(path, "r", encoding="utf-8") as f:
		data = yaml.safe_load(f) or {}
	entities = [Entity(**e) for e in data.get("entities", [])]
	dimensions = [Dimension(**d) for d in data.get("dimensions", [])]
	measures = [Measure(**m) for m in data.get("measures", [])]
	synonyms = data.get("synonyms", {})
	return Ontology(entities=entities, dimensions=dimensions, measures=measures, synonyms=synonyms)