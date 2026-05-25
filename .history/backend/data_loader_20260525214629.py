import pandas as pd

from backend.db_manager import engine

# --------------------------------
# LOAD CSV TO DATABASE
# --------------------------------

def load_csv_to_db(file_path):

    try:

        # READ CSV

        df = pd.read_csv(file_path)

        # CLEAN COLUMN NAMES

        df.columns = [
            col.strip().lower().replace(" ", "_")
            for col in df.columns
        ]

        # TABLE NAME

        table_name = "sales"

        # FORCE REPLACE TABLE

        df.to_sql(
            table_name,
            engine,
            if_exists="replace",
            index=False
        )

        # VERIFY TABLE CREATED

        test_query = pd.read_sql_query(
            "SELECT * FROM sales LIMIT 5",
            engine
        )

        return {

            "status": "success",

            "table_name": table_name,

            "rows": len(df),

            "columns": df.columns.tolist(),

            "preview": test_query.to_dict(
                orient="records"
            )
        }

    except Exception as e:

        return {

            "status": "error",

            "message": str(e)
        }