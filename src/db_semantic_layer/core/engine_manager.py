from __future__ import annotations

from typing import Dict, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from .config import settings

try:
	from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
	_OTEL_AVAILABLE = True
except Exception:  # pragma: no cover
	_OTEL_AVAILABLE = False


class EngineManager:
	def __init__(self) -> None:
		self._engines: Dict[str, Engine] = {}
		self._default_name: Optional[str] = settings.default_connection

	def create(self, name: str, url: str, echo: bool = False) -> Engine:
		engine = create_engine(url, echo=echo, future=True)
		if settings.telemetry_enabled and _OTEL_AVAILABLE:
			try:
				SQLAlchemyInstrumentor().instrument(engine=engine)
			except Exception:
				pass
		self._engines[name] = engine
		if self._default_name is None:
			self._default_name = name
		return engine

	def get(self, name: Optional[str] = None) -> Engine:
		if name is None:
			name = self._default_name
		if not name or name not in self._engines:
			raise KeyError("Engine nicht gefunden. Bitte Verbindung anlegen oder Namen angeben.")
		return self._engines[name]

	def list(self) -> Dict[str, str]:
		return {n: str(e.url) for n, e in self._engines.items()}

	def healthcheck(self, name: Optional[str] = None) -> bool:
		engine = self.get(name)
		with engine.connect() as conn:
			conn.execute(text("SELECT 1"))
		return True


def get_global_engine_manager() -> EngineManager:
	global _GLOBAL_ENGINE_MANAGER
	try:
		return _GLOBAL_ENGINE_MANAGER
	except NameError:
		_GLOBAL_ENGINE_MANAGER = EngineManager()
		return _GLOBAL_ENGINE_MANAGER