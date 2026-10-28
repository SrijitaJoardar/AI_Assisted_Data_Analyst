
from src.agent.answer_generator import generate_answer


if __name__ == "__main__":
    question = "Which region generated the highest total sales?"

    sql = """
    SELECT Region, SUM(Sales) AS Total_Sales
    FROM sales
    GROUP BY Region
    ORDER BY Total_Sales DESC
    LIMIT 1;
    """

    results = [
        {
            "Region": "West",
            "Total_Sales": 725457.8245,
        }
    ]

    answer = generate_answer(question, sql, results)

    print("\nUser question:")
    print(question)

    print("\nFinal answer:")
    print(answer)
