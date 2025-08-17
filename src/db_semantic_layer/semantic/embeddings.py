from __future__ import annotations

from typing import List
from litellm import embedding
from ..core.config import settings


class EmbeddingClient:
	def __init__(self, model: str | None = None) -> None:
		self.model = model or settings.embedding_model

	def embed(self, texts: List[str]) -> List[List[float]]:
		resp = embedding(model=self.model, input=texts)
		# litellm Antwort-Format kompatibel zu OpenAI
		vectors = [d["embedding"] for d in resp["data"]]
		return vectors