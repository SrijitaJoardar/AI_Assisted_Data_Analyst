
from unittest.mock import patch

from src.agent.answer_generator import generate_answer


def test_generate_answer_uses_actual_results():
    question = "Which region generated the highest total sales?"
    sql = "SELECT Region, SUM(Sales) AS Total_Sales FROM sales GROUP BY Region"

    results = [
        {"Region": "West", "Total_Sales": 725457.8245}
    ]

    with patch(
        "src.agent.answer_generator.generate_text",
        return_value="The West region generated the highest total sales.",
    ) as mock_generate_text:
        answer = generate_answer(question, sql, results)

    assert answer == "The West region generated the highest total sales."

    prompt = mock_generate_text.call_args.args[0]
    assert question in prompt
    assert sql in prompt
    assert "West" in prompt
    assert "725457.8245" in prompt


def test_generate_answer_handles_empty_results():
    answer = generate_answer(
        question="Which region generated the highest total sales?",
        sql="SELECT Region FROM sales WHERE 1 = 0",
        results=[],
    )

    assert answer == "No results were found for your question."
