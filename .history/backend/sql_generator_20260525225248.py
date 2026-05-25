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

    # --------------------------------
    # FIND SELECT QUERY
    # --------------------------------

    select_index = response.upper().find(
        "SELECT"
    )

    if select_index == -1:

        return ""

    sql_query = response[
        select_index:
    ].strip()

    # Remove accidental trailing text

    if ";" in sql_query:

        sql_query = (
            sql_query.split(";")[0]
            + ";"
        )

    return sql_query

# --------------------------------
# VALIDATE SQL
# --------------------------------

def validate_sql(sql_query):

    if not sql_query:

        return False

    sql_upper = sql_query.upper()

    # ONLY SELECT

    if not sql_upper.startswith(
        "SELECT"
    ):

        return False

    # BLOCK DANGEROUS SQL

    blocked_words = [

        "DROP",
        "DELETE",
        "UPDATE",
        "INSERT",
        "ALTER",
        "TRUNCATE"

    ]

    for word in blocked_words:

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

DATABASE SCHEMA:
{DATABASE_SCHEMA}

STRICT RULES:
1. Use ONLY tables from schema
2. NEVER invent tables
3. Use SQLite syntax ONLY
4. Return ONLY SQL
5. No explanation
6. No markdown
7. Query MUST start with SELECT
8. Use INNER JOIN when relationships exist
9. Use GROUP BY for aggregations
10. Use aliases like s and c

EXAMPLES:

Question:
Show customer_name and total sales

SQL:
SELECT c.customer_name,
SUM(s.sales) AS total_sales
FROM sales s
INNER JOIN customers c
ON s.customer_id = c.customer_id
GROUP BY c.customer_name;

Question:
Show total sales by region

SQL:
SELECT c.region,
SUM(s.sales) AS total_sales
FROM sales s
INNER JOIN customers c
ON s.customer_id = c.customer_id
GROUP BY c.region;

Question:
Show highest spending customers

SQL:
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

    # --------------------------------
    # GENERATE RESPONSE
    # --------------------------------

    response = generate_response(
        prompt
    )

    print(
        "\nRAW LLM RESPONSE:\n",
        response
    )

    # --------------------------------
    # CLEAN SQL
    # --------------------------------

    sql_query = clean_sql(
        response
    )

    print(
        "\nCLEANED SQL:\n",
        sql_query
    )

    # --------------------------------
    # VALIDATE
    # --------------------------------

    if validate_sql(
        sql_query
    ):

        return sql_query

    # --------------------------------
    # FALLBACK SMART QUERY
    # --------------------------------

    question_lower = user_question.lower()

    if "customer" in question_lower:

        return """
SELECT c.customer_name,
SUM(s.sales) AS total_sales
FROM sales s
INNER JOIN customers c
ON s.customer_id = c.customer_id
GROUP BY c.customer_name
ORDER BY total_sales DESC;
"""

    if "region" in question_lower:

        return """
SELECT c.region,
SUM(s.sales) AS total_sales
FROM sales s
INNER JOIN customers c
ON s.customer_id = c.customer_id
GROUP BY c.region;
"""

    return (
        "SELECT name "
        "FROM sqlite_master "
        "WHERE type='table';"
    )