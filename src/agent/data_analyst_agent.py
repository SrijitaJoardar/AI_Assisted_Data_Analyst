
import logging
from typing import TypedDict

from src.agent.sql_generator import generate_sql
from src.agent.answer_generator import generate_answer
from src.analytics.query_executor import run_query
from src.utils.formatters import format_currency


logger = logging.getLogger(__name__)


class AgentError(Exception):
    """Base exception for user-facing agent failures."""


class AIServiceError(AgentError):
    """Raised when an AI service call fails."""


class QueryExecutionError(AgentError):
    """Raised when SQL validation or execution fails."""


class AnalysisResult(TypedDict):
    """Structured output from a data analyst request."""

    sql: str
    results: list[dict]
    answer: str


def ask_data_analyst_detailed(question: str) -> AnalysisResult:
    """Return the generated SQL, database results, and final answer."""

    question = question.strip()

    if not question:
        raise ValueError("Please enter a question.")

    logger.info("Starting detailed data analyst request")

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
            "Unable to execute the generated query. "
            "Please try rephrasing your question."
        ) from error

    print("[3/3] Generating the final answer with Gemini...")

    try:
        answer = generate_answer(question, sql, results)


    except Exception:

        logger.exception("Answer generation failed")

        if results:

            readable_results = []

            for row in results:

                readable_row = {}

                for key, value in row.items():

                    if (

                            isinstance(value, (int, float))

                            and not isinstance(value, bool)

                            and key.casefold() in {

                        "sales",

                        "profit",

                        "total_sales",

                        "total_profit",

                    }

                    ):

                        readable_row[key] = format_currency(value)

                    else:

                        readable_row[key] = value

                readable_results.append(readable_row)

            answer = (

                "The database query succeeded, but Gemini is "

                "temporarily unavailable or its quota has been reached. "

                f"Here are the database results: {readable_results}"

            )

        else:

            answer = (

                "The database query succeeded, but Gemini is "

                "temporarily unavailable or its quota has been reached. "

                "The query returned no rows."

            )

    return {
        "sql": sql,
        "results": results,
        "answer": answer,
    }


def ask_data_analyst(question: str) -> str:
    """Answer a natural-language question using the sales database."""

    analysis = ask_data_analyst_detailed(question)
    return analysis["answer"]


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    question = "Which region generated the highest total sales?"

    print(f"\nQuestion: {question}")
    print("Analyzing your data...")

    try:
        analysis = ask_data_analyst_detailed(question)

        print(f"\nGenerated SQL:\n{analysis['sql']}")
        print(f"\nDatabase results:\n{analysis['results']}")
        print(f"\nAnswer: {analysis['answer']}")

    except AgentError as error:
        print(f"\nAgent error: {error}")

    except ValueError as error:
        print(f"\nInput error: {error}")
