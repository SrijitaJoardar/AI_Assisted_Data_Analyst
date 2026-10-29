
import pytest

from src.utils.formatters import (
    format_number,
    format_currency,
    format_percentage,
)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (725457.8245, "725,457.82"),
        (1000, "1,000.00"),
        (0, "0.00"),
        (-1234.5, "-1,234.50"),
    ],
)
def test_format_number(value, expected):
    assert format_number(value) == expected


def test_format_currency():
    assert format_currency(286408.34) == "₹286,408.34"


def test_format_percentage():
    assert format_percentage(14.94) == "14.94%"


def test_format_percentage_does_not_rescale_value():
    assert format_percentage(0.15) == "0.15%"


def test_format_number_handles_invalid_input():
    assert format_number("not-a-number") == "not-a-number"
