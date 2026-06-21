import pandas as pd

from backend.llm_engine import generate_response

# --------------------------------
# GENERATE AI INSIGHTS
# --------------------------------

def generate_insights(question, results):

    try:

        # --------------------------------
        # VALIDATION
        # --------------------------------

        if results is None:

            return "No results available."

        # Convert list to DataFrame

        if isinstance(results, list):

            df = pd.DataFrame(results)

        elif isinstance(results, pd.DataFrame):

            df = results

        else:

            return "Unsupported result format."

        # Empty DataFrame

        if df.empty:

            return "No data available."

        # --------------------------------
        # PREPARE DATA FOR GEMINI
        # --------------------------------

        data_preview = df.head(20).to_csv(
            index=False
        )

        prompt = f"""
You are a senior business analyst.

IMPORTANT RULES:

1. Use ONLY the data provided below.
2. Do NOT use external knowledge.
3. Do NOT invent facts.
4. Do NOT discuss industries, geography, economics, or trends unless explicitly present in the data.
5. Keep the analysis concise and professional.

BUSINESS QUESTION:
{question}

DATA:
{data_preview}

Provide:

1. Key Findings
2. Business Insights
3. Recommendations

Use bullet points only.
Maximum 8 bullets.
"""

        # --------------------------------
        # GEMINI ANALYSIS
        # --------------------------------

        ai_response = generate_response(
            prompt
        )

        if ai_response:

            ai_response = ai_response.strip()

            if len(ai_response) > 20:

                return ai_response

        # --------------------------------
        # FALLBACK INSIGHTS
        # --------------------------------

        insights = []

        numeric_cols = df.select_dtypes(
            include="number"
        ).columns.tolist()

        if numeric_cols:

            metric = numeric_cols[-1]

            insights.append(
                f"• Total {metric}: {df[metric].sum():,.2f}"
            )

            insights.append(
                f"• Average {metric}: {df[metric].mean():,.2f}"
            )

            insights.append(
                f"• Maximum {metric}: {df[metric].max():,.2f}"
            )

            insights.append(
                f"• Minimum {metric}: {df[metric].min():,.2f}"
            )

        object_cols = df.select_dtypes(
            include="object"
        ).columns.tolist()

        if object_cols:

            first_col = object_cols[0]

            try:

                top_item = (
                    df[first_col]
                    .value_counts()
                    .idxmax()
                )

                insights.append(
                    f"• Most frequent {first_col}: {top_item}"
                )

            except:

                pass

        if insights:

            return "\n".join(
                insights[:5]
            )

        return "No insights generated."

    except Exception as e:

        return f"Insight generation failed: {str(e)}"