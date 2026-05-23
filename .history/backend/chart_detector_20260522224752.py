import pandas as pd

def detect_chart_type(df):

    # Empty dataframe
    if df.empty:

        return None

    columns = df.columns.tolist()

    # Detect numeric columns
    numeric_cols = df.select_dtypes(
        include=["number"]
    ).columns.tolist()

    # Detect text columns
    text_cols = df.select_dtypes(
        include=["object"]
    ).columns.tolist()

    # Detect date columns
    for col in columns:

        if "date" in col.lower():

            if numeric_cols:

                return {

                    "chart": "line",

                    "x": col,

                    "y": numeric_cols[0]
                }

    # Detect bar chart
    if text_cols and numeric_cols:

        return {

            "chart": "bar",

            "x": text_cols[0],

            "y": numeric_cols[0]
        }

    return None