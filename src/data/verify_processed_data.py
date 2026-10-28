
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_FILE = (
    PROJECT_ROOT / "data" / "processed" / "superstore_sales_clean.csv"
)


def main() -> None:
    df = pd.read_csv(PROCESSED_FILE)

    print("--- Processed dataset verification ---")
    print(f"File exists: {PROCESSED_FILE.exists()}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print(f"Duplicate rows: {df.duplicated().sum()}")
    print(f"Missing values: {df.isnull().sum().sum()}")

    # CSV files do not preserve Pandas data types automatically.
    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        format="mixed",
        errors="raise",
    )

    print(f"Order Date type after conversion: {df['Order Date'].dtype}")
    print(f"Earliest date: {df['Order Date'].min()}")
    print(f"Latest date: {df['Order Date'].max()}")


if __name__ == "__main__":
    main()
