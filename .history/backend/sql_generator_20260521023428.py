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
You are an expert SQL generator.

Convert the user's question into a valid SQLite SQL query.

Rules:
1. Only generate SQL.
2. Do not explain anything.
3. Use only the provided schema.
4. Table name is sales.
5. Return ONLY SQL query text.

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