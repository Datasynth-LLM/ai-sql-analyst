from sqlalchemy import create_engine
import pandas as pd

DATABASE_URL = "sqlite:///database/sales.db"

engine = create_engine(DATABASE_URL)

def get_database_schema(table_name="sales"):

    try:

        # Read one row from database
        query = f"SELECT * FROM {table_name} LIMIT 1"

        df = pd.read_sql(query, engine)

        columns = df.columns.tolist()

        schema_text = f"""
Table Name: {table_name}

Columns:
"""

        for column in columns:

            schema_text += f"- {column}\n"

        return schema_text

    except Exception as e:

        return f"Schema Error: {str(e)}"