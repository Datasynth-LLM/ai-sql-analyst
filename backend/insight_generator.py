import pandas as pd

from backend.llm_engine import generate_response


# --------------------------------
# HELPER FUNCTIONS
# --------------------------------

def _build_summary(df):

    summary = []

    summary.append(f"Rows Returned: {len(df)}")
    summary.append(f"Columns Returned: {len(df.columns)}")

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    object_cols = df.select_dtypes(exclude="number").columns.tolist()

    # -----------------------------
    # Numeric analysis
    # -----------------------------

    for col in numeric_cols:

        summary.append("")

        summary.append(f"Metric: {col}")

        summary.append(
            f"Total = {df[col].sum():,.2f}"
        )

        summary.append(
            f"Average = {df[col].mean():,.2f}"
        )

        summary.append(
            f"Maximum = {df[col].max():,.2f}"
        )

        summary.append(
            f"Minimum = {df[col].min():,.2f}"
        )

        if len(df) > 1:

            max_row = df.loc[df[col].idxmax()]
            min_row = df.loc[df[col].idxmin()]

            for c in object_cols[:2]:

                if c in df.columns:

                    summary.append(
                        f"Highest {col}: {max_row[c]} ({max_row[col]:,.2f})"
                    )

                    summary.append(
                        f"Lowest {col}: {min_row[c]} ({min_row[col]:,.2f})"
                    )

                    break

    # -----------------------------
    # Missing values
    # -----------------------------

    missing = df.isna().sum().sum()

    summary.append("")
    summary.append(f"Missing Values: {missing}")

    return "\n".join(summary)


# --------------------------------
# FALLBACK INSIGHTS
# --------------------------------

def _fallback_insights(df):

    insights = []

    insights.append("📊 Key Findings")

    insights.append(
        f"• {len(df)} records were returned."
    )

    numeric_cols = df.select_dtypes(
        include="number"
    ).columns.tolist()

    object_cols = df.select_dtypes(
        exclude="number"
    ).columns.tolist()

    if numeric_cols:

        metric = numeric_cols[-1]

        highest = df.loc[
            df[metric].idxmax()
        ]

        lowest = df.loc[
            df[metric].idxmin()
        ]

        if object_cols:

            label = object_cols[0]

            insights.append(
                f"• Highest {metric}: {highest[label]} ({highest[metric]:,.2f})"
            )

            insights.append(
                f"• Lowest {metric}: {lowest[label]} ({lowest[metric]:,.2f})"
            )

        else:

            insights.append(
                f"• Maximum {metric}: {df[metric].max():,.2f}"
            )

            insights.append(
                f"• Minimum {metric}: {df[metric].min():,.2f}"
            )

        insights.append(
            f"• Average {metric}: {df[metric].mean():,.2f}"
        )

        insights.append("")

        insights.append("📈 Business Insights")

        insights.append(
            "• Results are generated directly from the returned SQL data."
        )

        insights.append(
            "• No external assumptions were used."
        )

        insights.append("")

        insights.append("🔍 Suggested Next Analysis")

        if object_cols:

            insights.append(
                f"• Compare {metric} across {object_cols[0]} over time."
            )

        else:

            insights.append(
                f"• Explore trends for {metric}."
            )

    return "\n".join(insights)


# --------------------------------
# MAIN FUNCTION
# --------------------------------

def generate_insights(question, results):

    try:

        if results is None:

            return "No results available."

        if isinstance(results, list):

            df = pd.DataFrame(results)

        elif isinstance(results, pd.DataFrame):

            df = results.copy()

        else:

            return "Unsupported result format."

        if df.empty:

            return "No data available."

        summary = _build_summary(df)

        table = df.head(20).to_markdown(index=False)

        prompt = f"""
        You are an experienced Business Intelligence Analyst.

        You must analyze ONLY the SQL query results provided.

        Your analysis MUST be completely grounded in the data.

        Never invent facts.

        Never assume causes.

        Never recommend loyalty programs, marketing strategies, pricing strategies, customer retention, operational improvements, or any information not directly supported by the data.

        Never mention SQL.

        Never repeat the user's question.

        Never restate the table.
        
        Use ONLY the statistics and SQL output below.

        Business Question:
        {question}

         Summary Statistics:
         {summary}

        SQL Result:
        {table}

        Write exactly these three sections.

        📊 Key Findings
        - Exactly 3 bullet points.
        - Mention the lowest value.
        - Mention one overall statistic such as average, total, range or record count.
        📈 Business Insights
        - Exactly 3 bullet points.
        - Only describe observable patterns in the returned data.
        - If the data is insufficient for deeper conclusions, explicitly say so.
        - Never speculate.

        🔍 Suggested Next Analysis
        - Exactly 2 bullet points.
        - Suggest analyses that naturally extend this result.
        - Do not give business advice.

        Rules:
        - Maximum 8 bullets total.
        - No paragraphs.
        - No markdown tables.
        - No code.
        - No assumptions.
        - No hallucinations.
        - Base every statement only on the supplied SQL results.
        """

        # --------------------------------
        # GENERATE AI INSIGHTS
        # --------------------------------

        ai_response = generate_response(prompt)

        print("\n========== GEMINI INSIGHTS ==========")
        print(ai_response)
        print("=====================================\n")

        if ai_response:

            cleaned = ai_response.strip()

            # Basic validation to avoid useless echoed responses
            bad_phrases = [
                "BUSINESS QUESTION",
                "SQL RESULT",
                "SQL RESULTS",
                "SELECT ",
                "FROM ",
                "How can we"
            ]

            upper = cleaned.upper()

            if (
                len(cleaned) > 40
                and not any(
                    phrase.upper() in upper
                    for phrase in bad_phrases
                )
            ):
                return cleaned

        print("Using Python fallback insights...")

        return _fallback_insights(df)

    except Exception as e:

        print("\n========== INSIGHT ERROR ==========")
        print(str(e))
        print("===================================\n")

        try:
            return _fallback_insights(df)
        except Exception:
            return f"Insight generation failed: {str(e)}"