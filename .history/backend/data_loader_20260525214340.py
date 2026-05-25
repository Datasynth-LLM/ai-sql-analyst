import pandas as pd

from backend.db_manager import engine

# --------------------------------
# LOAD CSV TO DATABASE
# --------------------------------

def load_csv_to_db(file_path):

    try:

        # Read CSV

        df = pd.read_csv(file_path)

        # Table Name

        table_name = "sales"

        # Store Into SQLite

        df.to_sql(
            table_name,
            engine,
            if_exists="replace",
            index=False
        )

        return {

            "status": "success",

            "table_name": table_name,

            "rows": len(df),

            "columns": df.columns.tolist()
        }

    except Exception as e:

        return {

            "status": "error",

            "message": str(e)
        }