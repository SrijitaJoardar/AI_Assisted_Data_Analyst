
import pytest

from src.analytics.query_executor import run_query


def test_query_returns_list_of_dictionaries():
    results = run_query(
        "SELECT Region FROM sales LIMIT 3"
    )

    assert isinstance(results, list)
    assert len(results) == 3
    assert all(isinstance(row, dict) for row in results)
    assert "Region" in results[0]


def test_aggregate_query_returns_expected_columns():
    results = run_query(
        "SELECT COUNT(*) AS total_rows FROM sales"
    )

    assert len(results) == 1
    assert results[0]["total_rows"] == 9992


def test_write_query_is_rejected():
    with pytest.raises(ValueError):
        run_query("DELETE FROM sales")


def test_unknown_table_is_rejected():
    with pytest.raises(ValueError):
        run_query("SELECT * FROM unknown_table")
