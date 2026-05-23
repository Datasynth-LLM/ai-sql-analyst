from backend.llm_engine import generate_response
from backend.schema_manager import get_database_schema

def extract_sql(response_text):

    """
    Extract only SQL query from LLM response.
    """

    lines = response_text.splitlines()

    sql_lines = []

    for line in lines:

        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Skip markdown
        if "```" in line:
            continue

        # Accept SQL starting keywords
        if line.upper().startswith((
            "SELECT",
            "WITH",
            "INSERT",
            "UPDATE",
            "DELETE"
        )):

            sql_lines.append(line)

    return " ".join(sql_lines)

def generate_sql(user_question):

    # Dynamic schema
    DATABASE_SCHEMA = get_database_schema()

    prompt = f"""
You are an SQLite expert.

Your task:
Generate ONLY a valid SQLite query.

STRICT RULES:
1. Return ONLY SQL
2. No explanation
3. No markdown
4. No comments
5. Use SQLite syntax only
6. Use LIMIT instead of TOP
7. Keep query simple
8. Use ONLY existing columns from schema

Database Schema:
{DATABASE_SCHEMA}

User Question:
{user_question}

SQL Query:
"""

    response = generate_response(prompt)

    # Clean response
    sql_query = extract_sql(response)

    return sql_query