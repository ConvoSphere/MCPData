from __future__ import annotations

from typing import Optional
from litellm import completion
from ..core.config import settings
from ..core.sql_validator import SQLValidator, SQLValidationError


SYSTEM_PROMPT = (
	"Du bist ein Assistent, der Nutzereingaben in SQL-SELECT-Abfragen übersetzt. "
	"Antwort ausschließlich mit SQL, ohne Erklärungen. Benutze nur erlaubte Tabellen/Spalten."
)


class NL2SQL:
	def __init__(self, dialect: Optional[str] = None) -> None:
		self.validator = SQLValidator(dialect=dialect)

	def generate_sql(self, question: str, schema_context: str) -> str:
		prompt = f"Kontext:\n{schema_context}\n\nFrage: {question}\nSQL:"
		resp = completion(model=settings.llm_model, messages=[
			{"role": "system", "content": SYSTEM_PROMPT},
			{"role": "user", "content": prompt},
		])
		text = resp["choices"][0]["message"]["content"].strip()
		try:
			return self.validator.validate_readonly(text)
		except SQLValidationError as e:
			raise e