from sqlalchemy import inspect

from backend.db_manager import engine
from backend.relationship_detector import (
    detect_relationships
)

# --------------------------------
# GET DATABASE SCHEMA
# --------------------------------

def get_database_schema():

    try:

        inspector = inspect(engine)

        tables = inspector.get_table_names()

        if not tables:

            return "No tables found."

        schema_text = ""

        # --------------------------------
        # TABLE SCHEMA
        # --------------------------------

        for table in tables:

            schema_text += (
                f"\nTable Name: {table}\n"
            )

            columns = inspector.get_columns(
                table
            )

            schema_text += "\nColumns:\n"

            for column in columns:

                schema_text += (
                    f"- {column['name']} "
                    f"({column['type']})\n"
                )

            schema_text += "\n"

        # --------------------------------
        # RELATIONSHIPS
        # --------------------------------

        relationships = detect_relationships()

        if relationships:

            schema_text += (
                "\nDetected Relationships:\n"
            )

            for rel in relationships:

                schema_text += (
                    f"- {rel['table1']}."
                    f"{rel['column']} "
                    f"<-> "
                    f"{rel['table2']}."
                    f"{rel['column']}\n"
                )

        return schema_text

    except Exception as e:

        return f"Schema Error: {str(e)}"