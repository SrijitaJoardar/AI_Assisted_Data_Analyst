
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_FILE = PROJECT_ROOT / "data" / "raw" / "superstore_sales.csv"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
PROCESSED_FILE = PROCESSED_DIR / "superstore_sales_clean.csv"


def load_raw_data() -> pd.DataFrame:
    """Load the original CSV file."""
    return pd.read_csv(RAW_FILE)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the dataset without modifying the original DataFrame."""
    cleaned_df = df.copy()

    # Convert order dates to proper datetime values.
    cleaned_df["Order Date"] = pd.to_datetime(
        cleaned_df["Order Date"],
        format="mixed",
        errors="raise",
    )

    # Remove rows that are exact duplicates across all columns.
    cleaned_df = cleaned_df.drop_duplicates().copy()

    return cleaned_df


def main() -> None:
    df = load_raw_data()
    cleaned_df = clean_data(df)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    cleaned_df.to_csv(PROCESSED_FILE, index=False)

    print("--- Cleaning summary ---")
    print(f"Original rows: {len(df)}")
    print(f"Cleaned rows: {len(cleaned_df)}")
    print(f"Rows removed: {len(df) - len(cleaned_df)}")
    print(f"Missing values remaining: {cleaned_df.isnull().sum().sum()}")
    print(f"Order Date data type: {cleaned_df['Order Date'].dtype}")
    print(f"Remaining duplicate rows: {cleaned_df.duplicated().sum()}")
    print(f"Processed file: {PROCESSED_FILE}")


if __name__ == "__main__":
    main()
