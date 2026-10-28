
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
You are a SQL assistant for a sales analytics application.

Database schema:
{DATABASE_SCHEMA}

Rules:
1. Generate a single SQLite SELECT query only.
2. Use only the table and columns listed in the schema.
3. Do not generate INSERT, UPDATE, DELETE, DROP, or other write operations.
4. Return only the SQL query, without Markdown fences or explanations.
5. If the question cannot be answered using this schema, do not invent columns.

User question:
{question}
"""

    sql = generate_text(prompt)
    return sql.strip()
