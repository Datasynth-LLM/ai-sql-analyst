import pandas as pd

def generate_insights(question, results):

    try:

        # --------------------------------
        # VALIDATION
        # --------------------------------

        if results is None:
            return "No results available."

        # Convert to DataFrame
        if isinstance(results, list):

            df = pd.DataFrame(results)

        elif isinstance(results, pd.DataFrame):

            df = results

        else:
            return "Unsupported result format."

        # Empty DataFrame
        if df.empty:
            return "No data available."

        insights = []

        columns = df.columns.tolist()

        # --------------------------------
        # SALES INSIGHTS
        # --------------------------------

        if "sales" in columns:

            max_sale = df["sales"].max()

            min_sale = df["sales"].min()

            total_sales = df["sales"].sum()

            insights.append(
                f"• Highest sales value recorded is {max_sale}."
            )

            insights.append(
                f"• Lowest sales value recorded is {min_sale}."
            )

            insights.append(
                f"• Total sales across results is {total_sales}."
            )

        # --------------------------------
        # REGION INSIGHTS
        # --------------------------------

        if "region" in columns:

            top_region = (
                df["region"]
                .value_counts()
                .idxmax()
            )

            insights.append(
                f"• Region appearing most frequently is {top_region}."
            )

        # --------------------------------
        # PRODUCT INSIGHTS
        # --------------------------------

        if "product" in columns:

            top_product = (
                df["product"]
                .value_counts()
                .idxmax()
            )

            insights.append(
                f"• Most common product in results is {top_product}."
            )

        # --------------------------------
        # CATEGORY INSIGHTS
        # --------------------------------

        if "category" in columns:

            top_category = (
                df["category"]
                .value_counts()
                .idxmax()
            )

            insights.append(
                f"• Most represented category is {top_category}."
            )

        # --------------------------------
        # QUANTITY INSIGHTS
        # --------------------------------

        if "quantity" in columns:

            total_quantity = df["quantity"].sum()

            insights.append(
                f"• Total quantity sold is {total_quantity}."
            )

        # --------------------------------
        # LIMIT INSIGHTS
        # --------------------------------

        insights = insights[:5]

        return "\n".join(insights)

    except Exception as e:

        return f"Insight generation failed: {str(e)}"