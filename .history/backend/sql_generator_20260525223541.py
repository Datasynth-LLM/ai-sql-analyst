from backend.llm_engine import generate_response
from backend.schema_manager import get_database_schema

# --------------------------------
# CLEAN SQL RESPONSE
# --------------------------------

def clean_sql(response):

    response = response.replace(
        "```sql",
        ""
    )

    response = response.replace(
        "```",
        ""
    )

    lines = response.splitlines()

    for line in lines:

        line = line.strip()

        if line.upper().startswith(
            "SELECT"
        ):

            return line

    return ""

# --------------------------------
# VALIDATE SQL
# --------------------------------

def validate_sql(sql_query):

    if not sql_query:

        return False

    sql_upper = sql_query.upper()

    # ONLY ALLOW SELECT

    if not sql_upper.startswith(
        "SELECT"
    ):

        return False

    # BLOCK DANGEROUS SQL

    blocked = [

        "DROP",
        "DELETE",
        "UPDATE",
        "INSERT",
        "ALTER",
        "TRUNCATE"

    ]

    for word in blocked:

        if word in sql_upper:

            return False

    return True

# --------------------------------
# GENERATE SQL
# --------------------------------

def generate_sql(user_question):

    DATABASE_SCHEMA = get_database_schema()

    prompt = f"""
You are an expert SQLite SQL generator.

IMPORTANT:
The database may contain MULTIPLE related tables.

STRICT RULES:
1. Use ONLY tables that exist in schema
2. NEVER invent fake tables
3. Use SQLite syntax only
4. Return ONLY SQL
5. No explanation
6. No markdown
7. Query must start with SELECT
8. Use correct table and column names
9. Use JOINS when relationships exist
10. Use intelligent aggregation when needed
11. Use GROUP BY when appropriate
12. Use aliases for readability

Database Schema:
{DATABASE_SCHEMA}

User Question:
{user_question}

SQL Query:
"""

    response = generate_response(
        prompt
    )

    sql_query = clean_sql(
        response
    )

    # --------------------------------
    # VALIDATE SQL
    # --------------------------------

    if not validate_sql(
        sql_query
    ):

        return (
            "SELECT name FROM "
            "sqlite_master "
            "WHERE type='table';"
        )

    return sql_query