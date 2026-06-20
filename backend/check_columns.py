from sqlalchemy import create_engine
import pandas as pd

engine = create_engine("sqlite:///database/sales.db")

query = "SELECT * FROM sales LIMIT 5"

df = pd.read_sql(query, engine)

print(df.columns)