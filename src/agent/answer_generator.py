
import json

from src.agent.llm_client import generate_text
from src.utils.formatters import format_currency


CURRENCY_FIELDS = {
    "sales",
    "profit",
    "total_sales",
    "total_profit",
}


def format_results_for_prompt(results: list[dict]) -> list[dict]:
    """Format known monetary fields for the AI prompt."""

    formatted_results = []

    for row in results:
        formatted_row = {}

        for key, value in row.items():
            if (
                isinstance(value, (int, float))
                and not isinstance(value, bool)
                and key.casefold() in CURRENCY_FIELDS
            ):
                formatted_row[key] = format_currency(value)
            else:
                formatted_row[key] = value

        formatted_results.append(formatted_row)

    return formatted_results


def generate_answer(
    question: str,
    sql: str,
    results: list[dict],
) -> str:
    """Generate a human-readable answer grounded in database results."""

    if not results:
        return "No matching records were found for your question."

    # Handle aggregate queries that return a row containing only NULL values.
    if all(value is None for row in results for value in row.values()):
        return (
            "The query returned no usable values. "
            "There may be no matching records for your question."
        )

    formatted_results = format_results_for_prompt(results)

    results_json = json.dumps(
        formatted_results,
        ensure_ascii=False,
        default=str,
    )

    prompt = f"""
You are a careful data analyst assistant.

Answer the user's question using only the SQL query and database
results provided below.

User question:
{question}

SQL query executed:
{sql}

Actual database results:
{results_json}

Rules:
1. Answer directly using the supplied results.
2. Never invent or change numerical values.
3. Do not claim that the data proves a cause unless the results support it.
4. Format large numbers with commas when appropriate.
5. Do not change monetary values already formatted in the results.
6. If the results do not fully answer the question, explain the limitation.
7. Use simple, professional English.
8. Return only the answer.
"""

    answer = generate_text(prompt)

    if not isinstance(answer, str) or not answer.strip():
        raise RuntimeError(
            "The AI service returned an empty or invalid answer."
        )

    return answer.strip()
