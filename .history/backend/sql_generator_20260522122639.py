from backend.llm_engine import generate_response
from backend.schema_manager import get_database_schema

def generate_sql(user_question):

    # Get dynamic schema
    DATABASE_SCHEMA = get_database_schema()

    prompt = f"""
You are an expert SQLite SQL generator.

Convert the user question into a SIMPLE valid SQLite SQL query.

DATABASE RULES:
- Use SQLite syntax only
- Use LIMIT instead of TOP
- Do NOT use markdown
- Do NOT explain anything
- Return ONLY SQL query text

IMPORTANT RULES:
- Keep queries simple
- Avoid unnecessary GROUP BY
- Avoid unnecessary subqueries
- Use case-insensitive filtering
- Use LOWER(column_name)
- Only use columns that exist in schema

Current Database Schema:
{DATABASE_SCHEMA}

User Question:
{user_question}
"""

    response = generate_response(prompt)

    # Remove markdown formatting
    response = response.replace(
        "```sql",
        ""
    )

    response = response.replace(
        "```",
        ""
    )

    return response.strip()