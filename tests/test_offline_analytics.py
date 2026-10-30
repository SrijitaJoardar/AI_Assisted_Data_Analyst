
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

def test_highest_profit_region():
    result = run_offline_analysis(
        "Which region generated the highest total profit?"
    )

    assert result is not None
    assert result["mode"] == "offline"
    assert "Region" in result["results"][0]
    assert "total_profit" in result["results"][0]
    assert len(result["results"]) == 1


def test_highest_sales_category():
    result = run_offline_analysis(
        "Which product category generated the highest sales?"
    )

    assert result is not None
    assert result["mode"] == "offline"
    assert "Category" in result["results"][0]
    assert "total_sales" in result["results"][0]
    assert len(result["results"]) == 1


def test_average_quantity_by_segment():
    result = run_offline_analysis(
        "What is the average quantity sold by segment?"
    )
    print("SQL:", result["sql"])
    print("Results:", result["results"])
    print("Answer:", result["answer"])

    assert result is not None
    assert result["mode"] == "offline"
    assert len(result["results"]) == 3
    assert "Segment" in result["results"][0]
    assert "average_quantity" in result["results"][0]
def test_maximum_sales_category():
    result = run_offline_analysis(
        "Which category had the maximum sales?"
    )

    assert result is not None
    assert result["mode"] == "offline"
    assert "Category" in result["results"][0]
    assert "total_sales" in result["results"][0]


def test_most_profit_region():
    result = run_offline_analysis(
        "Which region made the most profit?"
    )

    assert result is not None
    assert result["mode"] == "offline"
    assert "Region" in result["results"][0]
    assert "total_profit" in result["results"][0]


def test_mean_quantity_by_segment():
    result = run_offline_analysis(
        "Show the mean quantity for each segment."
    )

    assert result is not None
    assert result["mode"] == "offline"
    assert len(result["results"]) == 3
    assert "Segment" in result["results"][0]
    assert "average_quantity" in result["results"][0]