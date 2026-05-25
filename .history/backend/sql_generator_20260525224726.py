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

    response = response.strip()

    lines = response.splitlines()

    sql_lines = []

    capture = False

    for line in lines:

        line = line.strip()

        if line.upper().startswith(
            "SELECT"
        ):

            capture = True

        if capture:

            sql_lines.append(line)

    return " ".join(sql_lines)

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
You are a senior SQLite data analyst.

Your task is to generate accurate SQL queries.

DATABASE INFORMATION:
{DATABASE_SCHEMA}

VERY IMPORTANT RULES:

1. Use ONLY tables from schema
2. NEVER invent tables
3. Use ONLY SQLite syntax
4. Return ONLY SQL query
5. No markdown
6. No explanation
7. Query MUST start with SELECT
8. Use JOINS when relationships exist
9. Use aggregation when needed
10. Use GROUP BY when needed
11. Use aliases for readability
12. Prefer INNER JOIN when tables share IDs

EXAMPLES:

Question:
Show total sales by customer region

Correct SQL:
SELECT c.region,
SUM(s.sales) AS total_sales
FROM sales s
INNER JOIN customers c
ON s.customer_id = c.customer_id
GROUP BY c.region;

Question:
Show customer_name and total sales

Correct SQL:
SELECT c.customer_name,
SUM(s.sales) AS total_sales
FROM sales s
INNER JOIN customers c
ON s.customer_id = c.customer_id
GROUP BY c.customer_name;

Question:
Show highest spending customers

Correct SQL:
SELECT c.customer_name,
SUM(s.sales) AS total_sales
FROM sales s
INNER JOIN customers c
ON s.customer_id = c.customer_id
GROUP BY c.customer_name
ORDER BY total_sales DESC
LIMIT 10;

USER QUESTION:
{user_question}

SQL QUERY:
"""

    response = generate_response(
        prompt
    )

    sql_query = clean_sql(
        response
    )

    print(
        "\nGenerated SQL:\n",
        sql_query
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