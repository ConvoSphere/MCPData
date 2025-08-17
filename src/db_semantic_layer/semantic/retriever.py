from __future__ import annotations

from typing import List, Tuple
import math


def cosine_similarity(a: List[float], b: List[float]) -> float:
	dot = sum(x * y for x, y in zip(a, b))
	norm_a = math.sqrt(sum(x * x for x in a))
	norm_b = math.sqrt(sum(y * y for y in b))
	if norm_a == 0 or norm_b == 0:
		return 0.0
	return dot / (norm_a * norm_b)


class InMemoryVectorIndex:
	def __init__(self) -> None:
		self._items: List[Tuple[str, List[float]]] = []

	def add(self, key: str, vector: List[float]) -> None:
		self._items.append((key, vector))

	def search(self, query_vec: List[float], k: int = 5) -> List[Tuple[str, float]]:
		scored = [(key, cosine_similarity(vec, query_vec)) for key, vec in self._items]
		scored.sort(key=lambda x: x[1], reverse=True)
		return scored[:k]