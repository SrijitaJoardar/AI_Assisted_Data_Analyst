
from src.agent.sql_generator import generate_sql
from src.agent.answer_generator import generate_answer
from src.analytics.query_executor import run_query


def ask_data_analyst(question: str) -> str:
    """Answer a natural-language question using the sales database."""

    question = question.strip()

    if not question:
        raise ValueError("Please enter a question.")

    print("\n[1/3] Generating SQL with Gemini...")

    try:
        sql = generate_sql(question)
    except Exception as error:
        raise RuntimeError(
            f"SQL generation failed: {error}"
        ) from error

    print("[2/3] Validating and executing SQL...")

    try:
        results = run_query(sql)
    except Exception as error:
        raise RuntimeError(
            f"SQL validation or execution failed: {error}"
        ) from error

    print("[3/3] Generating the final answer with Gemini...")

    try:
        answer = generate_answer(question, sql, results)
    except Exception as error:
        raise RuntimeError(
            f"Answer generation failed: {error}"
        ) from error

    return answer


if __name__ == "__main__":
    question = "Which region generated the highest total sales?"

    print(f"\nQuestion: {question}")
    print("Analyzing your data...")

    try:
        answer = ask_data_analyst(question)
        print(f"\nAnswer: {answer}")

    except Exception as error:
        print(f"\nAgent error: {error}")
