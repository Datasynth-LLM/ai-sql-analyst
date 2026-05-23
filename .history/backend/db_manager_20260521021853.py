import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///database/sales.db"

engine = create_engine(DATABASE_URL)

def load_csv_to_db():
    df = pd.read_csv("data/sales_data.csv")

    df.to_sql(
        "sales",
        engine,
        if_exists="replace",
        index=False
    )

    print("Database created successfully!")

if __name__ == "__main__":
    load_csv_to_db()