from backend.llm_engine import generate_response
from backend.schema_manager import get_database_schema

# --------------------------------
# CLEAN SQL RESPONSE
# --------------------------------

def clean_sql(response):

    if not response:

        return ""

    response = response.replace(
        "```sql",
        ""
    )

    response = response.replace(
        "```",
        ""
    )

    response = response.strip()

    select_index = response.upper().find(
        "SELECT"
    )

    if select_index == -1:

        return ""

    sql_query = response[
        select_index:
    ].strip()

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

    if not sql_upper.startswith(
        "SELECT"
    ):

        return False

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
# RULE-BASED SQL ENGINE
# --------------------------------

def rule_based_sql(question):

    question = question.lower()

    # --------------------------------
    # CUSTOMER SALES
    # --------------------------------

    if (
        "customer_name" in question
        and
        "sales" in question
    ):

        return """
SELECT c.customer_name,
SUM(s.sales) AS total_sales
FROM sales s
INNER JOIN customers c
ON s.customer_id = c.customer_id
GROUP BY c.customer_name
ORDER BY total_sales DESC;
"""

    # --------------------------------
    # SALES BY REGION
    # --------------------------------

    if (
        "region" in question
        and
        "sales" in question
    ):

        return """
SELECT c.region,
SUM(s.sales) AS total_sales
FROM sales s
INNER JOIN customers c
ON s.customer_id = c.customer_id
GROUP BY c.region
ORDER BY total_sales DESC;
"""

    # --------------------------------
    # HIGHEST SPENDING CUSTOMERS
    # --------------------------------

    if (
        "highest spending" in question
        or
        "top customers" in question
    ):

        return """
SELECT c.customer_name,
SUM(s.sales) AS total_sales
FROM sales s
INNER JOIN customers c
ON s.customer_id = c.customer_id
GROUP BY c.customer_name
ORDER BY total_sales DESC
LIMIT 10;
"""

    # --------------------------------
    # TOTAL SALES
    # --------------------------------

    if "total sales" in question:

        return """
SELECT SUM(sales) AS total_sales
FROM sales;
"""

    # --------------------------------
    # DEFAULT
    # --------------------------------

    return None

# --------------------------------
# GENERATE SQL
# --------------------------------

def generate_sql(user_question):

    # --------------------------------
    # TRY RULE-BASED ENGINE FIRST
    # --------------------------------

    sql_query = rule_based_sql(
        user_question
    )

    if sql_query:

        return sql_query

    # --------------------------------
    # FALLBACK TO LLM
    # --------------------------------

    DATABASE_SCHEMA = get_database_schema()

    prompt = f"""
You are an expert SQLite SQL generator.

DATABASE SCHEMA:
{DATABASE_SCHEMA}

RULES:
1. Use ONLY schema tables
2. Return ONLY SQL
3. SQLite syntax only
4. Query must start with SELECT

QUESTION:
{user_question}

SQL:
"""

    try:

        response = generate_response(
            prompt
        )

        sql_query = clean_sql(
            response
        )

        if validate_sql(
            sql_query
        ):

            return sql_query

    except Exception as e:

        print(
            "LLM ERROR:",
            str(e)
        )

    # --------------------------------
    # FINAL SAFE FALLBACK
    # --------------------------------

    return """
SELECT name
FROM sqlite_master
WHERE type='table';
"""