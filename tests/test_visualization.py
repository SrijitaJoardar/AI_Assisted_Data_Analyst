import pytest

from src.analytics.visualization import create_bar_chart


def test_create_bar_chart_success():
    results = [
        {"Region": "West", "total_sales": 1000},
        {"Region": "East", "total_sales": 800},
    ]

    fig = create_bar_chart(results)

    assert fig is not None
    assert fig.data[0].x.tolist() == ["West", "East"]
    assert fig.data[0].y.tolist() == [1000, 800]


def test_create_bar_chart_returns_none_for_empty_results():
    assert create_bar_chart([]) is None


def test_create_bar_chart_returns_none_for_single_row():
    results = [{"Region": "West", "total_sales": 1000}]

    assert create_bar_chart(results) is None


def test_create_bar_chart_returns_none_for_multiple_numeric_columns():
    results = [
        {"Region": "West", "total_sales": 1000, "total_profit": 200},
        {"Region": "East", "total_sales": 800, "total_profit": 150},
    ]

    assert create_bar_chart(results) is None