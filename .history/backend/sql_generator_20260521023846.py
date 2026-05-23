from llm_engine import generate_response

DATABASE_SCHEMA = """
Table Name: sales

Columns:
- order_id
- customer_name
- product
- category
- region
- sales
- quantity
- order_date
"""

def generate_sql(user_question):

    prompt = f"""
You are an expert SQLite SQL generator.

Convert the user's question into a valid SQLite SQL query.

IMPORTANT SQLITE RULES:
1. Use LIMIT instead of TOP.
2. Only generate SQLite-compatible SQL.
3. Do not explain anything.
4. Return ONLY SQL query text.
5. Table name is sales.

Schema:
{DATABASE_SCHEMA}

User Question:
{user_question}
"""

    response = generate_response(prompt)

    # Clean markdown formatting
    response = response.replace("```sql", "")
    response = response.replace("```", "")

    return response.strip()