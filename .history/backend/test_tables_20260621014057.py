import pandas as pd

from backend.db_manager import engine

query = """
SELECT name
FROM sqlite_master
WHERE type='table';
"""

df = pd.read_sql_query(
    query,
    engine
)

print(df)