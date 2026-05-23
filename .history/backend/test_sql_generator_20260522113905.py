from backend.sql_generator import generate_sql

question = "Show top 5 highest sales"

sql_query = generate_sql(question)

print("\nGenerated SQL:\n")
print(sql_query)