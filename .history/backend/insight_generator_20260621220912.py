```python
import pandas as pd

from backend.llm_engine import generate_response

def generate_insights(question, results):

    try:

        # -----------------------------
        # VALIDATION
        # -----------------------------

        if results is None:

            return "No results available."

        if isinstance(results, list):

            df = pd.DataFrame(results)

        elif isinstance(results, pd.DataFrame):

            df = results

        else:

            return "Unsupported result format."

        if df.empty:

            return "No data available."

        # -----------------------------
        # LIMIT DATA SENT TO LLM
        # -----------------------------

        sample_data = df.head(10).to_string(
            index=False
        )

        prompt = f"""
You are a senior business analyst.

Business Question:
{question}

Query Results:
{sample_data}

Generate:

1. Key Findings
2. Business Insights
3. Recommendations

Keep response concise and professional.
"""

        ai_insights = generate_response(
            prompt
        )

        if ai_insights and len(ai_insights.strip()) > 20:

            return ai_insights

        # -----------------------------
        # FALLBACK INSIGHTS
        # -----------------------------

        insights = []

        numeric_cols = df.select_dtypes(
            include="number"
        ).columns.tolist()

        if numeric_cols:

            metric = numeric_cols[-1]

            insights.append(
                f"Total {metric}: {df[metric].sum():,.2f}"
            )

            insights.append(
                f"Average {metric}: {df[metric].mean():,.2f}"
            )

            insights.append(
                f"Maximum {metric}: {df[metric].max():,.2f}"
            )

        if len(df.columns) > 0:

            first_col = df.columns[0]

            if df[first_col].dtype == "object":

                top_item = (
                    df[first_col]
                    .value_counts()
                    .idxmax()
                )

                insights.append(
                    f"Most frequent {first_col}: {top_item}"
                )

        return "\n".join(insights)

    except Exception as e:

        return f"Insight generation failed: {str(e)}"
```
