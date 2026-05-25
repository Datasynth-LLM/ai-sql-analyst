import os
import pandas as pd

from sqlalchemy import create_engine

# --------------------------------
# CREATE DATABASE DIRECTORY
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

# --------------------------------
# DATABASE PATH
# --------------------------------

DATABASE_PATH = os.path.join(
    DATABASE_DIR,
    "analytics.db"
)

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

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
# RUN SQL QUERY
# --------------------------------

def run_sql_query(sql_query):

    try:

        df = pd.read_sql_query(
            sql_query,
            engine
        )

        return df

    except Exception as e:

        return str(e)