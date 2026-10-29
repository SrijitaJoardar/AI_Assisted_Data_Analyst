
from src.analytics.query_executor import run_query
from src.utils.formatters import format_currency


def run_offline_analysis(question: str) -> dict | None:
    """Answer supported questions using predefined SQL without an LLM."""

    normalized_question = " ".join(question.casefold().split())

    if (
        "highest total sales" in normalized_question
        and "region" in normalized_question
    ):
        sql = """
            SELECT Region, ROUND(SUM(Sales), 2) AS total_sales
            FROM sales
            GROUP BY Region
            ORDER BY total_sales DESC
            LIMIT 1
        """
        rows = run_query(sql)

        if not rows:
            answer = "No matching sales records were found."
        else:
            row = rows[0]
            answer = (
                f"The {row['Region']} region generated the highest "
                f"total sales, with {format_currency(row['total_sales'])}."
            )

    elif (
        "highest total profit" in normalized_question
        and "categor" in normalized_question
    ):
        sql = """
            SELECT Category, ROUND(SUM(Profit), 2) AS total_profit
            FROM sales
            GROUP BY Category
            ORDER BY total_profit DESC
            LIMIT 1
        """
        rows = run_query(sql)

        if not rows:
            answer = "No matching profit records were found."
        else:
            row = rows[0]
            answer = (
                f"{row['Category']} generated the highest total profit, "
                f"with {format_currency(row['total_profit'])}."
            )

    elif (
        "total sales" in normalized_question
        and "total profit" in normalized_question
    ):
        sql = """
            SELECT
                ROUND(SUM(Sales), 2) AS total_sales,
                ROUND(SUM(Profit), 2) AS total_profit
            FROM sales
        """
        rows = run_query(sql)

        if not rows or rows[0]["total_sales"] is None:
            answer = "No sales or profit records were found."
        else:
            row = rows[0]
            answer = (
                f"Total sales were {format_currency(row['total_sales'])}, "
                f"and total profit was {format_currency(row['total_profit'])}."
            )

    elif "sales by region" in normalized_question:
        sql = """
            SELECT Region, ROUND(SUM(Sales), 2) AS total_sales
            FROM sales
            GROUP BY Region
            ORDER BY total_sales DESC
        """
        rows = run_query(sql)

        if not rows:
            answer = "No matching sales records were found."
        else:
            answer = "Sales by region: " + "; ".join(
                f"{row['Region']}: {format_currency(row['total_sales'])}"
                for row in rows
            ) + "."

    elif (
        "lowest profit" in normalized_question
        and "sub-categor" in normalized_question
    ):
        sql = """
            SELECT
                "Sub-Category" AS sub_category,
                ROUND(SUM(Profit), 2) AS total_profit
            FROM sales
            GROUP BY "Sub-Category"
            ORDER BY total_profit ASC
            LIMIT 1
        """
        rows = run_query(sql)

        if not rows:
            answer = "No matching profit records were found."
        else:
            row = rows[0]
            answer = (
                f"{row['sub_category']} had the lowest total profit, "
                f"at {format_currency(row['total_profit'])}."
            )

    else:
        return None

    return {
        "sql": sql.strip(),
        "results": rows,
        "answer": answer,
        "mode": "offline",
    }
