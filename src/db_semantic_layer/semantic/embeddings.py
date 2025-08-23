from __future__ import annotations

from litellm import embedding

from ..core.config import settings


class EmbeddingClient:
	def __init__(self, model: str | None = None) -> None:
		self.model = model or settings.embedding_model

	def embed(self, texts: list[str]) -> list[list[float]]:
		resp = embedding(model=self.model, input=texts)
		# litellm Antwort-Format kompatibel zu OpenAI
		vectors = [d["embedding"] for d in resp["data"]]
		return vectors