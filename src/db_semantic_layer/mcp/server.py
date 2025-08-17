from __future__ import annotations

import asyncio
from typing import Optional
from mcp.server.fastmcp import FastMCP
from .tools import mcp
from ..utils.telemetry import init_telemetry


async def serve_stdio() -> None:
	await mcp.run()


async def serve_unix_socket(path: str) -> None:
	server = await mcp.create_unix_socket_server(path)
	async with server:
		await server.serve_forever()


async def serve_http(host: str = "127.0.0.1", port: int = 8081) -> None:
	server = await mcp.create_http_server(host=host, port=port)
	async with server:
		await server.serve_forever()


def run(server: str = "stdio", path: Optional[str] = None, host: str = "127.0.0.1", port: int = 8081) -> None:
	init_telemetry("dbsl-mcp")
	if server == "stdio":
		asyncio.run(serve_stdio())
	elif server == "unix":
		if not path:
			raise ValueError("Pfad für Unix-Socket erforderlich")
		asyncio.run(serve_unix_socket(path))
	elif server == "http":
		asyncio.run(serve_http(host=host, port=port))
	else:
		raise ValueError("Unbekannter Servertyp")