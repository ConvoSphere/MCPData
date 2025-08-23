from __future__ import annotations

import json
import re
import tempfile

import typer
import yaml
from rich import print
from sqlalchemy import text

from ..core.engine_manager import get_global_engine_manager
from ..core.schema_introspect import SchemaIntrospector
from ..core.sql_validator import SQLValidator
from ..mcp import server as mcp_server
from ..semantic.ontology_generation import build_schema_context, generate_ontology_yaml_from_context
from ..utils.telemetry import init_telemetry

init_telemetry("dbsl-cli")

app = typer.Typer(add_completion=True, help="DB Semantic Layer CLI")


@app.command()
def connect(name: str = typer.Argument(...), url: str = typer.Argument(...)) -> None:
	"""Erstellt eine benannte Verbindung."""
	mgr = get_global_engine_manager()
	mgr.create(name=name, url=url)
	print({"connected": name, "url": url})


@app.command()
def connections() -> None:
	"""Listet alle Verbindungen."""
	mgr = get_global_engine_manager()
	print(mgr.list())


@app.command()
def schema(name: str = typer.Option(None), db_schema: str = typer.Option(None, "--schema")) -> None:
	mgr = get_global_engine_manager()
	engine = mgr.get(name)
	ins = SchemaIntrospector(engine)
	snap = ins.snapshot(schema=db_schema)
	print(json.dumps(snap.model_dump(), indent=2))


@app.command()
def sql(query: str, name: str = typer.Option(None), safe: bool = typer.Option(True)) -> None:
	mgr = get_global_engine_manager()
	engine = mgr.get(name)
	validator = SQLValidator(dialect=engine.name)
	q = validator.validate_readonly(query) if safe else query
	with engine.connect() as conn:
		res = conn.execute(text(q))
		rows = res.fetchall()
		cols = list(res.keys())
	print(json.dumps({"columns": cols, "rows": [list(r) for r in rows]}, indent=2))


@app.command()
def ontology_generate(
	name: str = typer.Option(None, help="Verbindungsname"),
	db_schema: str = typer.Option(None, "--schema", help="DB-Schema/Namespace"),
	outfile: str = typer.Option(None, help="Pfad für Ausgabe-YAML; wenn leer, Ausgabe auf STDOUT"),
	language: str = typer.Option("de", help="Prompt-Sprache: de|en"),
	samples: int = typer.Option(0, help="Optional: pro Tabelle bis zu N Beispielzeilen in den Prompt aufnehmen"),
):
	"""Erzeugt per LLM eine Ontologie (YAML) aus dem DB-Schema."""
	mgr = get_global_engine_manager()
	engine = mgr.get(name)
	ins = SchemaIntrospector(engine)
	snap = ins.snapshot(schema=db_schema)
	# Optionales Tabellensampling
	sample_rows = None
	if samples and samples > 0:
		sample_rows = {}
		from sqlalchemy import text as _text
		with engine.connect() as conn:
			for t in ins.list_tables(schema=db_schema):
				fq_name = f"{db_schema}.{t.name}" if db_schema else t.name
				# Validate identifier parts conservatively to avoid SQL injection
				parts = fq_name.split(".")
				if not all(re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", p) for p in parts):
					print({"warning": f"Überspringe Tabelle mit ungültigem Namen: {fq_name}"})
					continue
				# Quote identifier parts using the dialect preparer
				quoted = ".".join(engine.dialect.identifier_preparer.quote(p) for p in parts)
				try:
					stmt = _text(f"SELECT * FROM {quoted} LIMIT :lim")  # nosec B608
					res = conn.execute(stmt, {"lim": int(samples)})
					cols = list(res.keys())
					rows = res.fetchall()
					sample_rows[t.name] = [dict(zip(cols, r, strict=False)) for r in rows]
				except Exception as exc:
					print({"warning": f"Sampling fehlgeschlagen für {fq_name}: {exc}"})
	
	schema_ctx = build_schema_context(schema=snap.model_dump(), samples=sample_rows)
	yaml_text = generate_ontology_yaml_from_context(schema_context=schema_ctx, language=language)
	# Validierung gegen Ontology-Modell (best-effort)
	from ..semantic.ontology import Ontology
	try:
		data = yaml.safe_load(yaml_text) or {}
		_ = Ontology(**data)
	except Exception as exc:
		print({"warning": f"YAML-Validierung fehlgeschlagen: {exc}"})
	if outfile:
		with open(outfile, "w", encoding="utf-8") as f:
			f.write(yaml_text)
		print({"written": outfile})
	else:
		print(yaml_text)


@app.command("mcp-serve")
def mcp_serve(
	server: str = typer.Option("unix", help="stdio|unix|http"),
	path: str = typer.Option(None, help="Unix-Socket Pfad"),
	host: str = typer.Option("127.0.0.1"),
	port: int = typer.Option(8081),
) -> None:
	if path is None:
		path = f"{tempfile.gettempdir()}/dbsl.sock"
	mcp_server.run(server=server, path=path, host=host, port=port)


if __name__ == "__main__":
	app()