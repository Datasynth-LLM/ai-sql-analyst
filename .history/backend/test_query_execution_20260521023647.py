from sql_generator import generate_sql
from db_manager import run_sql_query

question = "Show top 5 highest sales"

# Generate SQL
sql_query = generate_sql(question)

print("\nGenerated SQL:\n")
print(sql_query)

# Execute SQL
results = run_sql_query(sql_query)

print("\nQuery Results:\n")
print(results)