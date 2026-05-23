import pandas as pd

def detect_chart_type(df):

    try:

        # Ensure dataframe
        if not isinstance(df, pd.DataFrame):

            return None

        # Empty dataframe
        if df.empty:

            return None

        columns = df.columns.tolist()

        # Numeric columns
        numeric_cols = df.select_dtypes(
            include=["number"]
        ).columns.tolist()

        # Text columns
        text_cols = df.select_dtypes(
            include=["object"]
        ).columns.tolist()

        # Detect date-based chart
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

    except Exception:

        return None