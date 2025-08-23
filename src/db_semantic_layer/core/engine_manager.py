from __future__ import annotations

import logging

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from .config import settings

try:
	from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
	_OTEL_AVAILABLE = True
except Exception:  # pragma: no cover
	_OTEL_AVAILABLE = False


_GLOBAL_ENGINE_MANAGER: EngineManager | None = None


class EngineManager:
	def __init__(self) -> None:
		self._engines: dict[str, Engine] = {}
		self._default_name: str | None = settings.default_connection

	def create(self, name: str, url: str, echo: bool = False) -> Engine:
		engine = create_engine(url, echo=echo, future=True)
		if settings.telemetry_enabled and _OTEL_AVAILABLE:
			try:
				SQLAlchemyInstrumentor().instrument(engine=engine)
			except Exception as exc:
				logging.getLogger(__name__).warning("Failed to instrument SQLAlchemy engine: %s", exc)
		self._engines[name] = engine
		if self._default_name is None:
			self._default_name = name
		return engine

	def get(self, name: str | None = None) -> Engine:
		if name is None:
			name = self._default_name
		if not name or name not in self._engines:
			raise KeyError("Engine nicht gefunden. Bitte Verbindung anlegen oder Namen angeben.")
		return self._engines[name]

	def list(self) -> dict[str, str]:
		return {n: str(e.url) for n, e in self._engines.items()}

	def healthcheck(self, name: str | None = None) -> bool:
		engine = self.get(name)
		with engine.connect() as conn:
			conn.execute(text("SELECT 1"))
		return True


def get_global_engine_manager() -> EngineManager:
	global _GLOBAL_ENGINE_MANAGER
	if _GLOBAL_ENGINE_MANAGER is None:
		_GLOBAL_ENGINE_MANAGER = EngineManager()
	return _GLOBAL_ENGINE_MANAGER