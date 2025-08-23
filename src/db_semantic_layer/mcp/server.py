from __future__ import annotations


from ..utils.telemetry import init_telemetry
from .tools import mcp


def run(server: str = "stdio", path: str | None = None, host: str = "127.0.0.1", port: int = 8081) -> None:
	init_telemetry("dbsl-mcp")
	if server == "stdio":
		mcp.run()
	elif server == "unix":
		raise NotImplementedError("Unix socket server is not implemented for FastMCP")
	elif server == "http":
		raise NotImplementedError("HTTP server is not implemented for FastMCP")
	else:
		raise ValueError("Unbekannter Servertyp")