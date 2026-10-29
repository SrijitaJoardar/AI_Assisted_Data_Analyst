
from decimal import Decimal, InvalidOperation


def format_number(value: int | float | str) -> str:
    """Format a numeric value with commas and two decimal places."""

    try:
        number = Decimal(str(value))
        return f"{number:,.2f}"
    except (InvalidOperation, ValueError, TypeError):
        return str(value)


def format_currency(value: int | float | str) -> str:
    """Format a numeric value as Indian rupees."""

    return f"₹{format_number(value)}"


def format_percentage(value: int | float | str) -> str:
    """Format a percentage value without changing its scale."""

    return f"{format_number(value)}%"
