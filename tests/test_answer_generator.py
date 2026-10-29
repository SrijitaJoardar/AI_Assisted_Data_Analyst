
from unittest.mock import patch

import pytest

from src.agent.answer_generator import (
    generate_answer,
    format_results_for_prompt,
)


def test_generate_answer_uses_actual_results():
    question = "Which region generated the highest total sales?"
    sql = (
        "SELECT Region, SUM(Sales) AS Total_Sales "
        "FROM sales GROUP BY Region"
    )

    results = [
        {"Region": "West", "Total_Sales": 725457.8245}
    ]

    with patch(
        "src.agent.answer_generator.generate_text",
        return_value=(
            "The West region generated the highest total sales."
        ),
    ) as mock_generate_text:
        answer = generate_answer(question, sql, results)

    assert answer == (
        "The West region generated the highest total sales."
    )

    prompt = mock_generate_text.call_args.args[0]

    assert question in prompt
    assert sql in prompt
    assert "West" in prompt
    assert "₹725,457.82" in prompt


def test_generate_answer_handles_empty_results():
    answer = generate_answer(
        question="Which region generated the highest total sales?",
        sql="SELECT Region FROM sales WHERE 1 = 0",
        results=[],
    )

    assert answer == "No matching records were found for your question."


def test_generate_answer_rejects_empty_ai_response(monkeypatch):
    from src.agent import answer_generator

    monkeypatch.setattr(
        answer_generator,
        "generate_text",
        lambda prompt: "   ",
    )

    with pytest.raises(
        RuntimeError,
        match="empty or invalid answer",
    ):
        answer_generator.generate_answer(
            "Which region had the highest sales?",
            "SELECT Region FROM sales",
            [{"Region": "West"}],
        )


def test_generate_answer_strips_surrounding_whitespace(monkeypatch):
    from src.agent import answer_generator

    monkeypatch.setattr(
        answer_generator,
        "generate_text",
        lambda prompt: (
            "  The West region had the highest sales.  "
        ),
    )

    answer = answer_generator.generate_answer(
        "Which region had the highest sales?",
        "SELECT Region FROM sales",
        [{"Region": "West"}],
    )

    assert answer == "The West region had the highest sales."


def test_format_results_formats_monetary_fields():
    results = [
        {
            "Region": "West",
            "Total_Sales": 725457.8245,
            "Total_Profit": 108418.45,
        }
    ]

    formatted = format_results_for_prompt(results)

    assert formatted == [
        {
            "Region": "West",
            "Total_Sales": "₹725,457.82",
            "Total_Profit": "₹108,418.45",
        }
    ]


def test_format_results_does_not_modify_original_results():
    results = [
        {"Region": "West", "Total_Sales": 725457.8245}
    ]

    format_results_for_prompt(results)

    assert results[0]["Total_Sales"] == 725457.8245


def test_format_results_preserves_non_monetary_values():
    results = [
        {
            "Region": "West",
            "Quantity": 120,
            "Profit_Margin_Pct": 14.94,
        }
    ]

    formatted = format_results_for_prompt(results)

    assert formatted[0]["Quantity"] == 120
    assert formatted[0]["Profit_Margin_Pct"] == 14.94


def test_generate_answer_handles_null_aggregate_results():
    answer = generate_answer(
        question="What are the total sales for Atlantis?",
        sql=(
            "SELECT SUM(Sales) AS total_sales "
            "FROM sales WHERE Region = 'Atlantis'"
        ),
        results=[{"total_sales": None}],
    )

    assert "no usable values" in answer
