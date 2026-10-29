
from unittest.mock import patch

from src.agent.sql_generator import generate_sql


def test_generate_sql_returns_generated_query():
    question = "Which region generated the highest total sales?"

    expected_sql = (
        "SELECT Region, SUM(Sales) AS Total_Sales "
        "FROM sales GROUP BY Region ORDER BY Total_Sales DESC LIMIT 1"
    )

    with patch(
        "src.agent.sql_generator.generate_text",
        return_value=f"  {expected_sql}  ",
    ) as mock_generate_text:
        sql = generate_sql(question)

    assert sql == expected_sql

    prompt = mock_generate_text.call_args.args[0]
    assert question in prompt
    assert "sales" in prompt
    assert "Region" in prompt
    assert "Sales" in prompt
    assert "SQLite" in prompt


def test_generate_sql_preserves_generated_query_content():
    question = "Show total profit by category."
    expected_sql = (
        "SELECT Category, SUM(Profit) AS Total_Profit "
        "FROM sales GROUP BY Category"
    )

    with patch(
        "src.agent.sql_generator.generate_text",
        return_value=expected_sql,
    ):
        sql = generate_sql(question)

    assert sql == expected_sql
