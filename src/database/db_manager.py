
import sqlite3
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATABASE_DIR = PROJECT_ROOT / "database"
DATABASE_FILE = DATABASE_DIR / "superstore.db"

PROCESSED_FILE = (
    PROJECT_ROOT / "data" / "processed" / "superstore_sales_clean.csv"
)


def get_connection() -> sqlite3.Connection:
    """Create a connection to the SQLite database."""
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DATABASE_FILE)


def load_data_into_database() -> None:
    """Load the processed CSV into a SQLite table."""
    df = pd.read_csv(PROCESSED_FILE)

    connection = get_connection()

    try:
        df.to_sql(
            "sales",
            connection,
            if_exists="replace",
            index=False,
        )

        row_count = connection.execute(
            "SELECT COUNT(*) FROM sales"
        ).fetchone()[0]

        print(f"Database created: {DATABASE_FILE}")
        print(f"Rows loaded into sales table: {row_count}")

        print("\n--- Table columns ---")
        columns = connection.execute(
            "PRAGMA table_info(sales)"
        ).fetchall()

        for column in columns:
            print(f"{column[1]}: {column[2]}")

    finally:
        connection.close()


if __name__ == "__main__":
    load_data_into_database()
