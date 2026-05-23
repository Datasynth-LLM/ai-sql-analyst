import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///database/sales.db"

engine = create_engine(DATABASE_URL)

def load_csv_to_db(csv_path, table_name="sales"):

    try:

        # Read CSV
        df = pd.read_csv(csv_path)

        # Clean column names
        df.columns = [
            col.strip().lower().replace(" ", "_")
            for col in df.columns
        ]

        # Save to SQLite
        df.to_sql(
            table_name,
            engine,
            if_exists="replace",
            index=False
        )

        return {

            "status": "success",

            "table_name": table_name,

            "columns": list(df.columns),

            "rows": len(df)
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }