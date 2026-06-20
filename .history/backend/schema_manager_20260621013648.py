import pandas as pd
import os

from sqlalchemy import create_engine

# --------------------------------
# RENDER SAFE DATABASE DIRECTORY
# --------------------------------

BASE_DIR = "/tmp"

DATABASE_DIR = os.path.join(
    BASE_DIR,
    "database"
)

os.makedirs(
    DATABASE_DIR,
    exist_ok=True
)

# --------------------------------
# DATABASE PATH
# --------------------------------

DATABASE_PATH = os.path.join(
    DATABASE_DIR,
    "analytics.db"
)

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

print("\nSCHEMA DATABASE PATH:")
print(DATABASE_PATH)

# --------------------------------
# CREATE ENGINE
# --------------------------------

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False
    }
)

# --------------------------------
# GET DATABASE SCHEMA
# --------------------------------

def get_database_schema():

    try:

        tables_query = """
SELECT name
FROM sqlite_master
WHERE type='table';
"""

        tables_df = pd.read_sql(
            tables_query,
            engine
        )

        print("\nTABLES FOUND:")
        print(tables_df)

        if tables_df.empty:

            return "No tables found."

        schema_text = ""

        for table in tables_df["name"]:

            query = f"""
SELECT *
FROM {table}
LIMIT 1;
"""

            df = pd.read_sql(
                query,
                engine
            )

            schema_text += f"\nTable Name: {table}\n"
            schema_text += "Columns:\n"

            for col in df.columns:

                schema_text += f"- {col}\n"

        print("\nDATABASE SCHEMA:")
        print(schema_text)

        return schema_text

    except Exception as e:

        print("\nSCHEMA ERROR:")
        print(str(e))

        return f"Schema Error: {str(e)}"