from sqlalchemy import inspect

from backend.db_manager import engine

# --------------------------------
# DETECT RELATIONSHIPS
# --------------------------------

def detect_relationships():

    inspector = inspect(engine)

    tables = inspector.get_table_names()

    relationships = []

    # --------------------------------
    # GET TABLE COLUMNS
    # --------------------------------

    table_columns = {}

    for table in tables:

        columns = inspector.get_columns(table)

        table_columns[table] = [

            column["name"]

            for column in columns
        ]

    # --------------------------------
    # DETECT COMMON COLUMNS
    # --------------------------------

    for table1 in tables:

        for table2 in tables:

            if table1 == table2:

                continue

            cols1 = set(
                table_columns[table1]
            )

            cols2 = set(
                table_columns[table2]
            )

            common_columns = cols1.intersection(
                cols2
            )

            for column in common_columns:

                relationships.append({

                    "table1": table1,

                    "table2": table2,

                    "column": column
                })

    return relationships