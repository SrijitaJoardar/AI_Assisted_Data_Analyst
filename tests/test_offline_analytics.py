
from src.analytics.offline_analytics import run_offline_analysis


def test_highest_sales_region():
    result = run_offline_analysis(
        "Which region generated the highest total sales?"
    )

    assert result is not None
    assert result["mode"] == "offline"
    assert result["results"][0]["Region"] == "West"
    assert result["results"][0]["total_sales"] == 725457.82
    assert "West" in result["answer"]


def test_highest_profit_category():
    result = run_offline_analysis(
        "Which product category generated the highest total profit?"
    )

    assert result is not None
    assert result["results"][0]["Category"] == "Technology"
    assert result["results"][0]["total_profit"] == 145454.95
    assert "Technology" in result["answer"]


def test_total_sales_and_profit():
    result = run_offline_analysis(
        "What are the total sales and total profit?"
    )

    assert result is not None
    assert result["results"][0]["total_sales"] == 2296914.56
    assert result["results"][0]["total_profit"] == 286408.34


def test_sales_by_region():
    result = run_offline_analysis("Show sales by region")

    assert result is not None
    assert len(result["results"]) == 4
    assert result["results"][0]["Region"] == "West"


def test_lowest_profit_subcategory():
    result = run_offline_analysis(
        "Which sub-category generated the lowest profit?"
    )

    assert result is not None
    assert result["results"][0]["sub_category"] == "Tables"
    assert result["results"][0]["total_profit"] == -17725.48


def test_unsupported_question_returns_none():
    result = run_offline_analysis(
        "What is the average order quantity for each customer?"
    )

    assert result is None
