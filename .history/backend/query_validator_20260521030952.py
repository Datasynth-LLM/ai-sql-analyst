FORBIDDEN_KEYWORDS = [
    "DROP",
    "DELETE",
    "UPDATE",
    "INSERT",
    "ALTER",
    "TRUNCATE",
    "CREATE"
]

def validate_query(query):

    upper_query = query.upper()

    for keyword in FORBIDDEN_KEYWORDS:

        if keyword in upper_query:
            return False

    return True