
from unittest.mock import Mock, patch

import pytest
from google.genai import errors

from src.agent import llm_client


def make_api_error(status_code: int) -> errors.APIError:
    """Create a simulated Google API error."""
    return errors.APIError(
        code=status_code,
        response_json={
            "error": {
                "code": status_code,
                "message": "Simulated API error",
                "status": "UNAVAILABLE",
            }
        },
    )


@patch("src.agent.llm_client.time.sleep")
@patch("src.agent.llm_client.random.uniform", return_value=0)
@patch("src.agent.llm_client.get_gemini_client")
def test_generate_text_retries_after_503(
    mock_get_client,
    mock_random,
    mock_sleep,
):
    client = Mock()
    mock_get_client.return_value = client

    client.models.generate_content.side_effect = [
        make_api_error(503),
        Mock(text="  SQL retrieves data.  "),
    ]

    result = llm_client.generate_text("Explain SQL")

    assert result == "SQL retrieves data."
    assert client.models.generate_content.call_count == 2
    mock_sleep.assert_called_once_with(1)


@patch("src.agent.llm_client.time.sleep")
@patch("src.agent.llm_client.get_gemini_client")
def test_generate_text_stops_after_max_attempts(
    mock_get_client,
    mock_sleep,
):
    client = Mock()
    mock_get_client.return_value = client

    client.models.generate_content.side_effect = [
        make_api_error(503),
        make_api_error(503),
        make_api_error(503),
    ]

    with pytest.raises(RuntimeError, match="remained unavailable"):
        llm_client.generate_text("Explain SQL")

    assert client.models.generate_content.call_count == 3
    assert mock_sleep.call_count == 2
