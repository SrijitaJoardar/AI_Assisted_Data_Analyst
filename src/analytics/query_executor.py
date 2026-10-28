
import sqlite3
from pathlib import Path
from src.agent.sql_validator import validate_sql


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATABASE_FILE = PROJECT_ROOT / "database" / "superstore.db"



def run_query(sql: str) -> list[dict]:
    """Validate a query, execute it, and return rows as dictionaries."""
    is_valid, message = validate_sql(sql)

    if not is_valid:
        raise ValueError(message)

    connection = sqlite3.connect(
        f"file:{DATABASE_FILE.as_posix()}?mode=ro",
        uri=True,
    )
    connection.row_factory = sqlite3.Row

    try:
        cursor = connection.execute(sql)
        return [dict(row) for row in cursor.fetchall()]
    finally:
        connection.close()



def display_results(title: str, sql: str) -> None:
    """Execute a query and display its returned data."""
    print(f"\n--- {title} ---")

    results = run_query(sql)

    if not results:
        print("No results found.")
        return

    # Display column headers.
    print(" | ".join(results[0].keys()))
    print("-" * 70)

    for row in results:
        print(" | ".join(str(value) for value in row.values()))


if __name__ == "__main__":
    display_results(
        "Overall sales and profit",
        """
        SELECT
            ROUND(SUM(Sales), 2) AS total_sales,
            ROUND(SUM(Profit), 2) AS total_profit,
            SUM(Quantity) AS total_quantity
        FROM sales
        """,
    )

    display_results(
        "Sales by region",
        """
        SELECT
            Region,
            ROUND(SUM(Sales), 2) AS total_sales
        FROM sales
        GROUP BY Region
        ORDER BY total_sales DESC
        """,
    )

    display_results(
        "Profit by category",
        """
        SELECT
            Category,
            ROUND(SUM(Profit), 2) AS total_profit
        FROM sales
        GROUP BY Category
        ORDER BY total_profit DESC
        """,
    )

    display_results(
        "Profit by sub-category",
        """
        SELECT
            [Sub-Category],
            ROUND(SUM(Sales), 2) AS total_sales,
            ROUND(SUM(Profit), 2) AS total_profit
        FROM sales
        GROUP BY [Sub-Category]
        ORDER BY total_profit ASC
        LIMIT 5
        """,
    )

    display_results(
        "Sales and profit by region",
        """
        SELECT
            Region,
            ROUND(SUM(Sales), 2) AS total_sales,
            ROUND(SUM(Profit), 2) AS total_profit,
            ROUND(
                SUM(Profit) * 100.0 / SUM(Sales),
                2
            ) AS profit_margin_pct
        FROM sales
        GROUP BY Region
        ORDER BY total_profit DESC
        """,
    )

    display_results(
        "Profit by customer segment",
        """
        SELECT
            Segment,
            ROUND(SUM(Sales), 2) AS total_sales,
            ROUND(SUM(Profit), 2) AS total_profit
        FROM sales
        GROUP BY Segment
        ORDER BY total_profit DESC
        """,
    )
