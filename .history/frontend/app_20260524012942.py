import pandas as pd

def detect_chart_type(df):

    try:

        # -----------------------------
        # Validate dataframe
        # -----------------------------

        if not isinstance(df, pd.DataFrame):

            return None

        if df.empty:

            return None

        columns = df.columns.tolist()

        # -----------------------------
        # Numeric columns
        # -----------------------------

        numeric_cols = df.select_dtypes(
            include=["number"]
        ).columns.tolist()

        # Remove IDs
        numeric_cols = [

            col for col in numeric_cols

            if "id" not in col.lower()
        ]

        # -----------------------------
        # Text columns
        # -----------------------------

        text_cols = df.select_dtypes(
            include=["object"]
        ).columns.tolist()

        # -----------------------------
        # DATE LINE CHART
        # -----------------------------

        for col in columns:

            if "date" in col.lower():

                if "sales" in numeric_cols:

                    return {

                        "chart": "line",

                        "x": col,

                        "y": "sales"
                    }

        # -----------------------------
        # PIE CHART
        # -----------------------------

        for category_col in [

            "category",
            "region",
            "product"
        ]:

            if category_col in columns:

                for value_col in [

                    "sales",
                    "quantity"
                ]:

                    if value_col in numeric_cols:

                        unique_values = df[
                            category_col
                        ].nunique()

                        if unique_values <= 8:

                            return {

                                "chart": "pie",

                                "x": category_col,

                                "y": value_col
                            }

        # -----------------------------
        # SCATTER PLOT
        # -----------------------------

        if len(numeric_cols) >= 2:

            return {

                "chart": "scatter",

                "x": numeric_cols[0],

                "y": numeric_cols[1]
            }

        # -----------------------------
        # BAR CHART
        # -----------------------------

        preferred_x = None

        for col in [

            "region",
            "category",
            "product",
            "customer_name"
        ]:

            if col in columns:

                preferred_x = col

                break

        preferred_y = None

        for col in [

            "sales",
            "quantity",
            "revenue",
            "profit"
        ]:

            if col in numeric_cols:

                preferred_y = col

                break

        if preferred_x and preferred_y:

            return {

                "chart": "bar",

                "x": preferred_x,

                "y": preferred_y
            }

        # -----------------------------
        # FALLBACK
        # -----------------------------

        if text_cols and numeric_cols:

            return {

                "chart": "bar",

                "x": text_cols[0],

                "y": numeric_cols[0]
            }

        return None

    except Exception as e:

        print("Chart Detection Error:", e)

        return None