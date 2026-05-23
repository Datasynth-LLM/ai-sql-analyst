import pandas as pd
from sqlalchemy import create_engine

DATABASE_PATH = "database/sales.db"

engine = create_engine(f"sqlite:///{DATABASE_PATH}")

def load_csv_to_db():

    df = pd.read_csv("data/sales_data.csv")

    df.to_sql(
        "sales",
        engine,
        if_exists="replace",
        index=False
    )

    print("Database created successfully!")

def run_sql_query(query):

    try:
        df = pd.read_sql(query, engine)
        return df

    except Exception as e:
        return str(e)

if __name__ == "__main__":
    load_csv_to_db()