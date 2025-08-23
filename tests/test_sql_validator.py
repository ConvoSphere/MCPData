import pytest

from db_semantic_layer.core.sql_validator import SQLValidationError, SQLValidator


def test_validator_allows_select_and_enforces_limit():
	v = SQLValidator(dialect="sqlite", enforce_limit=100)
	res = v.validate_readonly("select 1")
	assert "limit" in res.lower()


def test_validator_blocks_non_select():
	v = SQLValidator(dialect="sqlite")
	with pytest.raises(SQLValidationError):
		v.validate_readonly("delete from x")