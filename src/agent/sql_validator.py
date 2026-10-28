
import sqlite3


ALLOWED_TABLES = {"sales"}

FORBIDDEN_KEYWORDS = {
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "CREATE",
    "REPLACE",
    "ATTACH",
    "DETACH",
    "PRAGMA",
    "VACUUM",
}


def validate_sql(sql: str) -> tuple[bool, str]:
    """
    Perform basic validation of a single read-only SELECT query.

    Returns:
        (True, message) if the query passes these checks.
        (False, reason) if it fails.
    """
    if not sql or not sql.strip():
        return False, "SQL query cannot be empty."

    query = sql.strip()

    # Allow at most one optional trailing semicolon.
    if ";" in query.rstrip(";"):
        return False, "Multiple SQL statements are not allowed."

    query = query.rstrip(";").strip()

    if not query.upper().startswith("SELECT"):
        return False, "Only SELECT queries are allowed."

    # Reject SQL comments in this beginner-level validator.
    if "--" in query or "/*" in query or "*/" in query:
        return False, "SQL comments are not allowed."

    # Reject obvious modifying or administrative keywords.
    tokens = query.upper().replace("(", " ").replace(")", " ").split()

    for token in tokens:
        keyword = token.strip(",;")
        if keyword in FORBIDDEN_KEYWORDS:
            return False, f"Forbidden SQL keyword: {keyword}"

    # Restrict table references to the approved table.
    # This is a basic check, not a full SQL parser.
    connection = None

    try:
        connection = sqlite3.connect(":memory:")
        connection.execute(
            "CREATE TABLE sales ("
            '"Order Date" TEXT, Region TEXT, State TEXT, '
            'Category TEXT, "Sub-Category" TEXT, Segment TEXT, '
            "Sales REAL, Profit REAL, Quantity INTEGER)"
        )

        connection.execute(
            "CREATE VIEW allowed_sales AS SELECT * FROM sales"
        )

        # SQLite will catch syntax errors here, but schema validation
        # against the real database happens in the execution layer.
        connection.execute("EXPLAIN " + query)
    except sqlite3.Error as exc:
        return False, f"SQL syntax or validation error: {exc}"
    finally:
        if connection is not None:
            connection.close()

    return True, "SQL passed basic validation."
