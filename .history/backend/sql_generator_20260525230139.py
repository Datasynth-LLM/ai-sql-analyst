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

    # ONLY ALLOW SELECT

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
# RULE-BASED SQL ENGINE
# --------------------------------

def rule_based_sql(question, tables):

    question = question.lower()

    sales_table = None
    customer_table = None

    # --------------------------------
    # DETECT TABLE NAMES
    # --------------------------------

    for table in tables:

        lower_table = table.lower()

        if "sales" in lower_table:

            sales_table = table

        if "customer" in lower_table:

            customer_table = table

    print("\nDETECTED TABLES:")
    print(tables)

    print("\nSALES TABLE:")
    print(sales_table)

    print("\nCUSTOMER TABLE:")
    print(customer_table)

    # --------------------------------
    # CUSTOMER SALES
    # --------------------------------

    if (
        "customer_name" in question
        and
        "sales" in question
    ):

        if sales_table and customer_table:

            return f"""
SELECT c.customer_name,
SUM(s.sales) AS total_sales
FROM {sales_table} s
INNER JOIN {customer_table} c
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

        if sales_table and customer_table:

            return f"""
SELECT c.region,
SUM(s.sales) AS total_sales
FROM {sales_table} s
INNER JOIN {customer_table} c
ON s.customer_id = c.customer_id
GROUP BY c.region
ORDER BY total_sales DESC;
"""

    # --------------------------------
    # TOP CUSTOMERS
    # --------------------------------

    if (
        "highest spending" in question
        or
        "top customers" in question
    ):

        if sales_table and customer_table:

            return f"""
SELECT c.customer_name,
SUM(s.sales) AS total_sales
FROM {sales_table} s
INNER JOIN {customer_table} c
ON s.customer_id = c.customer_id
GROUP BY c.customer_name
ORDER BY total_sales DESC
LIMIT 10;
"""

    # --------------------------------
    # TOTAL SALES
    # --------------------------------

    if (
        "total sales" in question
        and
        sales_table
    ):

        return f"""
SELECT SUM(sales) AS total_sales
FROM {sales_table};
"""

    return None

# --------------------------------
# GENERATE SQL
# --------------------------------

def generate_sql(user_question):

    DATABASE_SCHEMA = get_database_schema()

    print("\nDATABASE SCHEMA:\n")
    print(DATABASE_SCHEMA)

    # --------------------------------
    # DETECT TABLES
    # --------------------------------

    tables = detect_tables(
        DATABASE_SCHEMA
    )

    # --------------------------------
    # TRY RULE ENGINE
    # --------------------------------

    sql_query = rule_based_sql(
        user_question,
        tables
    )

    if sql_query:

        print("\nFINAL GENERATED SQL:\n")
        print(sql_query)

        return sql_query

    # --------------------------------
    # FALLBACK TO LLM
    # --------------------------------

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

        print("\nRAW LLM RESPONSE:\n")
        print(response)

        sql_query = clean_sql(
            response
        )

        print("\nCLEANED SQL:\n")
        print(sql_query)

        if validate_sql(
            sql_query
        ):

            return sql_query

    except Exception as e:

        print(
            "\nLLM ERROR:\n",
            str(e)
        )

    # --------------------------------
    # FINAL FALLBACK
    # --------------------------------

    return """
SELECT name
FROM sqlite_master
WHERE type='table';
"""