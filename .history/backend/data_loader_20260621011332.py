import pandas as pd
import os

from sqlalchemy import create_engine

# --------------------------------
# DATABASE SETUP
# --------------------------------

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATABASE_DIR = os.path.join(
    BASE_DIR,
    "database"
)

os.makedirs(
    DATABASE_DIR,
    exist_ok=True
)

DATABASE_PATH = os.path.join(
    DATABASE_DIR,
    "analytics.db"
)

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False
    }
)

# --------------------------------
# LOAD CSV
# --------------------------------

def load_csv_to_db(file_path):

    try:

        df = pd.read_csv(
            file_path
        )

        table_name = os.path.basename(
            file_path
        )

        table_name = table_name.replace(
            ".csv",
            ""
        )

        table_name = table_name.replace(
            " ",
            "_"
        )

        table_name = table_name.lower()

        df.to_sql(

            table_name,

            engine,

            if_exists="replace",

            index=False
        )

        print("\nTABLE SAVED:")
        print(table_name)

        print("\nROWS:")
        print(len(df))

        print("\nCOLUMNS:")
        print(df.columns.tolist())

        return {

            "status": "success",

            "table_name": table_name,

            "rows": len(df),

            "columns": df.columns.tolist()
        }

    except Exception as e:

        print("\nCSV LOAD ERROR:")
        print(str(e))

        return {

            "status": "error",

            "message": str(e)
        }