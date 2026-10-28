
import pytest

from src.agent.sql_validator import validate_sql


def test_select_query_is_allowed():
    valid, _ = validate_sql("SELECT Region FROM sales")
    assert valid is True


def test_empty_query_is_rejected():
    valid, _ = validate_sql("")
    assert valid is False


def test_delete_query_is_rejected():
    valid, _ = validate_sql("DELETE FROM sales")
    assert valid is False


def test_multiple_statements_are_rejected():
    valid, _ = validate_sql(
        "SELECT * FROM sales; DELETE FROM sales;"
    )
    assert valid is False


def test_unknown_table_is_rejected():
    valid, _ = validate_sql("SELECT * FROM unknown_table")
    assert valid is False


@pytest.mark.parametrize(
    "sql",
    [
        "UPDATE sales SET Profit = 0",
        "DROP TABLE sales",
        "INSERT INTO sales (Region) VALUES ('Test')",
        "DELETE FROM sales",
        "PRAGMA table_info(sales)",
    ],
)
def test_modifying_or_administrative_queries_are_rejected(sql):
    valid, _ = validate_sql(sql)
    assert valid is False


def test_query_with_trailing_semicolon_is_allowed():
    valid, _ = validate_sql("SELECT Region FROM sales;")
    assert valid is True


def test_nonexistent_column_is_rejected():
    valid, _ = validate_sql("SELECT unknown_column FROM sales")
    assert valid is False
