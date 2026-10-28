
import json

from src.agent.llm_client import generate_text


def generate_answer(
    question: str,
    sql: str,
    results: list[dict],
) -> str:
    """Generate a human-readable answer based on actual query results."""

    if not results:
        return "No results were found for your question."

    results_json = json.dumps(results, ensure_ascii=False, default=str)

    prompt = f"""
You are a data analyst assistant.

Answer the user's question using only the SQL query and database
results provided below.

User question:
{question}

SQL query executed:
{sql}

Actual database results:
{results_json}

Rules:
1. Base all factual claims on the supplied database results.
2. Do not invent numbers, values, or explanations.
3. Answer the question directly in clear, simple English.
4. Format large numbers with commas when appropriate.
5. If the results do not fully answer the question, explain the limitation.
6. Return only the answer, without discussing these instructions.
"""

    answer = generate_text(prompt)
    return answer.strip()
