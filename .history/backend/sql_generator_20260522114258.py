from backend.llm_engine import generate_response

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

Convert the user question into a SIMPLE valid SQLite SQL query.

DATABASE RULES:
- Table name is sales
- Use SQLite syntax only
- Use LIMIT instead of TOP
- Do NOT use markdown
- Do NOT explain anything
- Return ONLY SQL query text

IMPORTANT:
- Keep queries simple
- Avoid unnecessary GROUP BY
- Avoid subqueries unless required
- Use ORDER BY sales DESC LIMIT 5 for top sales queries

Schema:
{DATABASE_SCHEMA}

User Question:
{user_question}
"""

    response = generate_response(prompt)

    # Remove markdown formatting
    response = response.replace("```sql", "")
    response = response.replace("```", "")

    return response.strip()