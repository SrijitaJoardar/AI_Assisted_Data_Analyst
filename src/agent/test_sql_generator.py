
from src.agent.sql_generator import generate_sql
from src.analytics.query_executor import run_query


if __name__ == "__main__":
    question = "Which region generated the highest total sales?"

    print("\nUser question:")
    print(question)

    # Step 1: Generate SQL using Gemini.
    sql = generate_sql(question)

    print("\nGenerated SQL:")
    print(sql)

    # Step 2: Execute the SQL through the existing query executor.
    # The executor should validate the query before execution.
    print("\nExecuting SQL...")

    try:
        results = run_query(sql)

        print("\nQuery results:")
        for row in results:
            print(row)

    except Exception as error:
        print(f"Query failed: {error}")
