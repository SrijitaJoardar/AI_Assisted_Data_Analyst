
import sqlite3


ALLOWED_TABLES = {"sales"}

ALLOWED_COLUMNS = {
    "Order Date",
    "Region",
    "State",
    "Category",
    "Sub-Category",
    "Segment",
    "Sales",
    "Profit",
    "Quantity",
}

ALLOWED_FUNCTIONS = {
    "COUNT",
    "SUM",
    "AVG",
    "MIN",
    "MAX",
    "ROUND",
    "ABS",
    "LOWER",
    "UPPER",
    "COALESCE",
    "IFNULL",
}

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


def _authorize_read_only(
    action: int,
    arg1: str | None,
    arg2: str | None,
    database_name: str | None,
    trigger_name: str | None,
) -> int:
    """Allow approved read-only queries against the sales table."""

    if action == sqlite3.SQLITE_SELECT:
        return sqlite3.SQLITE_OK

    if action == sqlite3.SQLITE_READ:
        table_name = (arg1 or "").casefold()
        column_name = (arg2 or "").casefold()

        allowed_tables = {
            name.casefold() for name in ALLOWED_TABLES
        }
        allowed_columns = {
            name.casefold() for name in ALLOWED_COLUMNS
        }

        if (
            table_name in allowed_tables
            and (
                column_name in allowed_columns
                or column_name == ""
            )
        ):
            return sqlite3.SQLITE_OK

        return sqlite3.SQLITE_DENY

    if action == sqlite3.SQLITE_FUNCTION:
        function_name = (arg2 or arg1 or "").upper()

        if function_name in ALLOWED_FUNCTIONS:
            return sqlite3.SQLITE_OK

        return sqlite3.SQLITE_DENY

    # Deny writes, schema changes, and all other actions.
    return sqlite3.SQLITE_DENY


def validate_sql(sql: str) -> tuple[bool, str]:
    """
    Validate a single read-only SELECT query.

    Returns:
        (True, message) if validation succeeds.
        (False, reason) if validation fails.
    """

    if not sql or not sql.strip():
        return False, "SQL query cannot be empty."

    query = sql.strip()

    # Allow one optional trailing semicolon.
    if query.endswith(";"):
        query = query[:-1].rstrip()

    if not query:
        return False, "SQL query cannot be empty."

    # Reject multiple SQL statements.
    if ";" in query:
        return False, "Multiple SQL statements are not allowed."

    # This validator supports SELECT queries only.
    if not query.upper().startswith("SELECT"):
        return False, "Only SELECT queries are allowed."

    # Reject SQL comments.
    if "--" in query or "/*" in query or "*/" in query:
        return False, "SQL comments are not allowed."

    # Reject obvious modifying or administrative keywords.
    tokens = (
        query.upper()
        .replace("(", " ")
        .replace(")", " ")
        .split()
    )

    for token in tokens:
        keyword = token.strip(",;")

        if keyword in FORBIDDEN_KEYWORDS:
            return False, f"Forbidden SQL keyword: {keyword}"

    connection = None

    try:
        connection = sqlite3.connect(":memory:")

        # Create a temporary schema for syntax and column checks.
        connection.execute(
            'CREATE TABLE sales ('
            '"Order Date" TEXT, '
            'Region TEXT, '
            'State TEXT, '
            'Category TEXT, '
            '"Sub-Category" TEXT, '
            'Segment TEXT, '
            'Sales REAL, '
            'Profit REAL, '
            'Quantity INTEGER)'
        )

        # Apply the read-only authorization rules.
        connection.set_authorizer(_authorize_read_only)

        # EXPLAIN checks query compilation without returning data.
        connection.execute("EXPLAIN " + query)

    except sqlite3.Error as exc:
        return False, f"SQL syntax or validation error: {exc}"

    finally:
        if connection is not None:
            connection.close()

    return True, "SQL passed read-only validation."
