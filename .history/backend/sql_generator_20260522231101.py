from backend.llm_engine import generate_response
from backend.schema_manager import get_database_schema

VALID_SQL_STARTERS = (
    "SELECT",
    "WITH"
)

def extract_sql(response_text):

    """
    Extract valid SQL only.
    """

    lines = response_text.splitlines()

    for line in lines:

        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Remove markdown
        if "```" in line:
            continue

        # Accept only SQL starters
        upper_line = line.upper()

        if upper_line.startswith(VALID_SQL_STARTERS):

            return line

    return ""

def validate_sql(sql_query):

    """
    Validate generated SQL.
    """

    if not sql_query:

        return False

    sql_upper = sql_query.upper()

    # Allow only SELECT/WITH
    if not sql_upper.startswith(VALID_SQL_STARTERS):

        return False

    # Block dangerous queries
    blocked_keywords = [

        "DROP",
        "DELETE",
        "UPDATE",
        "INSERT",
        "ALTER",
        "TRUNCATE"
    ]

    for keyword in blocked_keywords:

        if keyword in sql_upper:

            return False

    return True

def generate_sql(user_question):

    DATABASE_SCHEMA = get_database_schema()

    prompt = f"""
Generate ONLY a valid SQLite SELECT query.

STRICT RULES:
- Return ONLY SQL
- No explanation
- No markdown
- No comments
- Use SQLite syntax only
- Use LIMIT instead of TOP
- Use ONLY schema columns
- Query must start with SELECT

Database Schema:
{DATABASE_SCHEMA}

User Question:
{user_question}

SQL:
"""

    response = generate_response(prompt)

    sql_query = extract_sql(response)

    # Validate SQL
    if not validate_sql(sql_query):

        # Safe fallback query
        return "SELECT * FROM sales LIMIT 5;"

    return sql_query