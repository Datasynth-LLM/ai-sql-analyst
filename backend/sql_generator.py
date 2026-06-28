import os
import pandas as pd
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
# DETECT TABLES
# --------------------------------

def detect_tables(schema_text):

    tables = []

    lines = schema_text.splitlines()

    for line in lines:

        line = line.strip()

        if line.startswith(
            "Table Name:"
        ):

            table = line.split(
                ":"
            )[1].strip()

            tables.append(table)

    return tables


# --------------------------------
# RULE BASED SQL
# --------------------------------

def rule_based_sql(question, tables):

    question = question.lower()

    sales_table = None

    for table in tables:

        if "sales" in table.lower():

            sales_table = table

            break

    print("\nSALES TABLE:")
    print(sales_table)

    if not sales_table:
        return None

    # --------------------------------
    # SHOW ALL TABLES
    # --------------------------------

    if "show all tables" in question:

        return """
SELECT
    name AS available_tables
FROM sqlite_master
WHERE type='table'
ORDER BY name;
"""

    # --------------------------------
    # TOP CUSTOMERS
    # --------------------------------

    if (
        "top customers" in question
        or
        "highest spending" in question
    ):

        return f"""
SELECT
    customer_name,
    SUM(sales) AS total_sales
FROM {sales_table}
GROUP BY customer_name
ORDER BY total_sales DESC
LIMIT 10;
"""

    # --------------------------------
    # SALES BY REGION
    # --------------------------------

    if (
        "region" in question
        and
        "sales" in question
    ):

        return f"""
SELECT
    region,
    SUM(sales) AS total_sales
FROM {sales_table}
GROUP BY region
ORDER BY total_sales DESC;
"""

    # --------------------------------
    # SALES BY CATEGORY
    # --------------------------------

    if (
        "category" in question
        and
        "sales" in question
    ):

        return f"""
SELECT
    category,
    SUM(sales) AS total_sales
FROM {sales_table}
GROUP BY category
ORDER BY total_sales DESC;
"""

    # --------------------------------
    # CUSTOMER SALES
    # --------------------------------

    if (
        "customer" in question
        and
        "sales" in question
    ):

        return f"""
SELECT
    customer_name,
    SUM(sales) AS total_sales
FROM {sales_table}
GROUP BY customer_name
ORDER BY total_sales DESC;
"""

    # --------------------------------
    # TOP PRODUCTS
    # --------------------------------

    if (
        "top products" in question
        or
        "best selling" in question
        or
        "product sales" in question
    ):

        return f"""
SELECT
    product,
    SUM(sales) AS total_sales
FROM {sales_table}
GROUP BY product
ORDER BY total_sales DESC
LIMIT 10;
"""

    # --------------------------------
    # AVERAGE SALES BY REGION
    # --------------------------------

    if (
        "average sales" in question
        and
        "region" in question
    ):

        return f"""
SELECT
    region,
    AVG(sales) AS average_sales
FROM {sales_table}
GROUP BY region
ORDER BY average_sales DESC;
"""

    # --------------------------------
    # HIGHEST SALE
    # --------------------------------

    if (
        "highest sale" in question
        or
        "largest sale" in question
    ):

        return f"""
SELECT *
FROM {sales_table}
ORDER BY sales DESC
LIMIT 1;
"""

    # --------------------------------
    # TOTAL SALES
    # --------------------------------

    if "total sales" in question:

        return f"""
SELECT
    SUM(sales) AS total_sales
FROM {sales_table};
"""

    return None


# --------------------------------
# GENERATE SQL
# --------------------------------

def generate_sql(user_question):

    DATABASE_SCHEMA = get_database_schema()

    print("\nDATABASE SCHEMA:")
    print(DATABASE_SCHEMA)

    tables = detect_tables(
        DATABASE_SCHEMA
    )

    sql_query = rule_based_sql(
        user_question,
        tables
    )

    if sql_query:

        print("\nRULE SQL:")
        print(sql_query)

        return sql_query

    prompt = f"""
You are an expert SQLite SQL generator.

DATABASE SCHEMA:

{DATABASE_SCHEMA}

RULES:
1. Use ONLY schema tables
2. Return ONLY SQL
3. SQLite syntax only
4. Query must start with SELECT
5. Never explain the SQL

QUESTION:
{user_question}

SQL:
"""

    try:

        response = generate_response(
            prompt
        )

        print("\nRAW RESPONSE:")
        print(response)

        sql_query = clean_sql(
            response
        )

        print("\nCLEANED SQL:")
        print(sql_query)

        if validate_sql(
            sql_query
        ):

            return sql_query

    except Exception as e:

        print(
            "\nLLM ERROR:",
            str(e)
        )

    return """
SELECT
    name AS available_tables
FROM sqlite_master
WHERE type='table'
ORDER BY name;
"""

