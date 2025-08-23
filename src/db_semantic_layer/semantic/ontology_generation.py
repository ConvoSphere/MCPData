from __future__ import annotations

from typing import Any

from ..core.config import settings


def _extract_yaml_block(text: str) -> str:
	"""Extract YAML content from an LLM response.

	- If a fenced block ```yaml ... ``` is present, return its inner content.
	- If a generic fenced block ``` ... ``` is present, return its inner content.
	- Otherwise, return the full text.
	"""
	start_yaml = text.find("```yaml")
	if start_yaml != -1:
		start_yaml += len("```yaml")
		end = text.find("```", start_yaml)
		if end != -1:
			return text[start_yaml:end].strip()
	# fallback: any fenced block
	start = text.find("```")
	if start != -1:
		start += len("```")
		end = text.find("```", start)
		if end != -1:
			return text[start:end].strip()
	return text.strip()


def build_schema_context(
	schema: dict[str, Any],
	samples: dict[str, list[dict[str, Any]]] | None = None,
) -> str:
	"""Build a concise, LLM-friendly schema context string from a schema snapshot dict.

	The expected schema dict structure follows `SchemaSnapshot.model_dump()`.
	"""
	tables = schema.get("tables", [])
	lines: list[str] = []
	for t in tables:
		name = t.get("name")
		cols = ", ".join(f"{c.get('name')}:{c.get('type')}" for c in t.get("columns", []))
		pk_cols = ", ".join(t.get("primary_key", []) or [])
		fk_map = t.get("foreign_keys", {}) or {}
		fk_str = ", ".join(f"{col}->{ref}" for col, ref in fk_map.items()) if fk_map else ""
		meta_parts = []
		if pk_cols:
			meta_parts.append(f"pk=[{pk_cols}]")
		if fk_str:
			meta_parts.append(f"fks=[{fk_str}]")
		meta = f" ({'; '.join(meta_parts)})" if meta_parts else ""
		lines.append(f"{name}: {cols}{meta}")
		if samples and name in samples and samples[name]:
			lines.append(f"samples {name}:")
			for row in samples[name][:3]:
				# Display as key=value pairs for compactness
				pair_str = ", ".join(f"{k}={v}" for k, v in row.items())
				lines.append(f"- {pair_str}")
	return "\n".join(lines)


def generate_ontology_yaml_from_context(
	schema_context: str,
	llm_model: str | None = None,
	language: str = "de",
) -> str:
	"""Call the LLM via litellm to produce ontology YAML from a schema context string."""
	# Lazy import to avoid hard dependency at import time
	from litellm import completion

	model_name = llm_model or settings.llm_model
	if language.lower().startswith("de"):
		system = (
			"Du erzeugst eine Ontologie für einen Semantik-Layer im YAML-Format. "
			"Antworte ausschließlich mit YAML und nutze die Schlüssel: entities, dimensions, measures, synonyms. "
			"Ordne Entities realen Tabellen zu (table) und Measures auf gültige Aggregationsausdrücke. Keine Erklärungen."
		)
		user = (
			"Gegebenes Datenbank-Schema (mit optionalen Datenbeispielen):\n"
			f"{schema_context}\n\n"
			"Gib ausschließlich YAML zurück mit folgender Struktur:\n"
			"entities: [{name, description?, table, primary_key?}]\n"
			"dimensions: [{name, description?, column}]\n"
			"measures: [{name, description?, expression}]\n"
			"synonyms: {<term>: [<syn1>, <syn2>] }\n"
			"Nutze nur existierende Tabellen- und Spaltennamen."
		)
	else:
		system = (
			"You generate a semantic layer ontology in YAML. "
			"Respond with YAML only using keys: entities, dimensions, measures, synonyms. "
			"Map entities to real tables and measures to valid SQL aggregations. No explanations."
		)
		user = (
			"Given the database schema (with optional samples):\n"
			f"{schema_context}\n\n"
			"Return YAML only with structure as above. Use existing table/column names."
		)

	resp = completion(
		model=model_name,
		messages=[
			{"role": "system", "content": system},
			{"role": "user", "content": user},
		],
	)
	content = resp["choices"][0]["message"]["content"].strip()
	return _extract_yaml_block(content)

