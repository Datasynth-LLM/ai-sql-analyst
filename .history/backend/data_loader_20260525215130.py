import os
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

        # --------------------------------
        # DYNAMIC TABLE NAME
        # --------------------------------

        file_name = os.path.basename(file_path)

        table_name = os.path.splitext(
            file_name
        )[0]

        table_name = table_name.lower().replace(
            " ",
            "_"
        )

        # --------------------------------
        # STORE TABLE
        # --------------------------------

        df.to_sql(
            table_name,
            engine,
            if_exists="replace",
            index=False
        )

        # --------------------------------
        # VERIFY TABLE
        # --------------------------------

        preview = pd.read_sql_query(
            f"SELECT * FROM {table_name} LIMIT 5",
            engine
        )

        return {

            "status": "success",

            "table_name": table_name,

            "rows": len(df),

            "columns": df.columns.tolist(),

            "preview": preview.to_dict(
                orient="records"
            )
        }

    except Exception as e:

        return {

            "status": "error",

            "message": str(e)
        }