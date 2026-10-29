
import logging

from src.agent.sql_generator import generate_sql
from src.agent.answer_generator import generate_answer
from src.analytics.query_executor import run_query


logger = logging.getLogger(__name__)


class AgentError(Exception):
    """Base exception for user-facing agent failures."""


class AIServiceError(AgentError):
    """Raised when an AI service call fails."""


class QueryExecutionError(AgentError):
    """Raised when SQL validation or execution fails."""


def ask_data_analyst(question: str) -> str:
    """Answer a natural-language question using the sales database."""

    question = question.strip()

    if not question:
        raise ValueError("Please enter a question.")

    logger.info("Starting data analyst request")

    print("\n[1/3] Generating SQL with Gemini...")

    try:
        sql = generate_sql(question)
    except Exception as error:
        logger.exception("SQL generation failed")
        raise AIServiceError(
            "Unable to generate SQL right now. Please try again shortly."
        ) from error

    print("[2/3] Validating and executing SQL...")

    try:
        results = run_query(sql)
    except Exception as error:
        logger.exception("SQL validation or execution failed")
        raise QueryExecutionError(
            "Unable to execute the generated query. Please try rephrasing your question."
        ) from error

    print("[3/3] Generating the final answer with Gemini...")

    try:
        answer = generate_answer(question, sql, results)
    except Exception as error:
        logger.exception("Answer generation failed")
        # The query already succeeded, so preserve the actual results.
        return (
            "The database query succeeded, but I couldn't generate a "
            f"natural-language explanation. Raw results: {results}"
        )

    return answer


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    question = "Which region generated the highest total sales?"

    print(f"\nQuestion: {question}")
    print("Analyzing your data...")

    try:
        answer = ask_data_analyst(question)
        print(f"\nAnswer: {answer}")

    except AgentError as error:
        print(f"\nAgent error: {error}")

    except ValueError as error:
        print(f"\nInput error: {error}")
