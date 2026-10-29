
from src.agent.llm_client import generate_text


DATABASE_SCHEMA = """
Table name: sales

Columns:
- Order Date: order date stored as text
- Region: sales region
- State: state name
- Category: product category
- Sub-Category: product sub-category
- Segment: customer segment
- Sales: sales amount
- Profit: profit amount
- Quantity: quantity sold
"""


def generate_sql(question: str) -> str:
    """Generate a SQL query from a user's natural-language question."""

    prompt = f"""
You are a careful SQL assistant for a sales analytics application.

Database schema:
{DATABASE_SCHEMA}

Rules:
1. Generate exactly one SQLite SELECT query.
2. Use only the sales table and the columns listed in the schema.
3. Never generate INSERT, UPDATE, DELETE, DROP, or other write operations.
4. Return only SQL, without Markdown fences or explanations.
5. Do not invent tables or columns.
6. For SUM, AVG, MIN, or MAX queries, consider what happens when
   no rows match the WHERE condition.
7. When the question asks for a total and you use SUM, use COALESCE
   only when returning zero for no matching rows is appropriate.
8. Do not assume that a missing region, category, or state exists.
9. For questions asking which group has the highest or lowest value,
   use GROUP BY and appropriate ORDER BY and LIMIT clauses.
10. Use aliases that clearly identify calculated values.

User question:
{question}
"""

    sql = generate_text(prompt)
    return sql.strip()
