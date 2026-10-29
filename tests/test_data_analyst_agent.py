
from unittest.mock import patch

import pytest

from src.agent.data_analyst_agent import (
    AIServiceError,
    QueryExecutionError,
    ask_data_analyst,
)


def test_empty_question_is_rejected():
    with pytest.raises(ValueError, match="Please enter a question"):
        ask_data_analyst("   ")


@patch("src.agent.data_analyst_agent.generate_sql")
def test_sql_generation_failure_returns_agent_error(mock_generate_sql):
    mock_generate_sql.side_effect = RuntimeError("Simulated API failure")

    with pytest.raises(AIServiceError, match="Unable to generate SQL"):
        ask_data_analyst("Which region has the highest sales?")


@patch("src.agent.data_analyst_agent.generate_sql")
@patch("src.agent.data_analyst_agent.run_query")
def test_query_failure_returns_agent_error(mock_run_query, mock_generate_sql):
    mock_generate_sql.return_value = "SELECT Region FROM sales"
    mock_run_query.side_effect = ValueError("Simulated SQL validation failure")

    with pytest.raises(QueryExecutionError, match="Unable to execute"):
        ask_data_analyst("Show sales by region")
