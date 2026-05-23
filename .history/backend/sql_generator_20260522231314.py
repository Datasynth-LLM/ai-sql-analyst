from backend.llm_engine import generate_response
from backend.schema_manager import get_database_schema

VALID_SQL_STARTERS = (
    "SELECT",
)

ALLOWED_COLUMNS = [
    "order_id",
    "customer_name",
    "product",
    "category",
    "region",
    "sales",
    "quantity",
    "order_date"
]

TABLE_NAME = "sales"

def clean_sql(response):

    """
    Clean LLM SQL response.
    """

    response = response.replace("```sql", "")
    response = response.replace("```", "")

    lines = response.splitlines()

    for line in lines:

        line = line.strip()

        if line.upper().startswith("SELECT"):

            return line

    return ""

def validate_sql(sql_query):

    """
    Validate SQL safety and schema.
    """

    if not sql_query:

        return False

    sql_upper = sql_query.upper()

    # Only SELECT allowed
    if not sql_upper.startswith("SELECT"):

        return False

    # Block dangerous SQL
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

    # Block fake tables
    fake_tables = [

        "CUSTOMERS",
        "PRODUCTS",
        "ORDERS",
        "CATEGORIES",
        "REGIONS"
    ]

    for table in fake_tables:

        if table in sql_upper:

            return False

    return True

def generate_sql(user_question):

    DATABASE_SCHEMA = get_database_schema()

    prompt = f"""
You are an SQLite SQL generator.

IMPORTANT:
The database has ONLY ONE table:
sales

Allowed columns:
- order_id
- customer_name
- product
- category
- region
- sales
- quantity
- order_date

STRICT RULES:
1. Use ONLY table: sales
2. NEVER invent tables
3. NEVER use joins
4. NEVER use customers/products/orders tables
5. Use SQLite syntax only
6. Return ONLY SQL
7. No explanation
8. No markdown
9. Query must start with SELECT

Example:
SELECT * FROM sales ORDER BY sales DESC LIMIT 5;

Database Schema:
{DATABASE_SCHEMA}

User Question:
{user_question}

SQL Query:
"""

    response = generate_response(prompt)

    sql_query = clean_sql(response)

    # Validate query
    if not validate_sql(sql_query):

        return "SELECT * FROM sales LIMIT 5;"

    return sql_query