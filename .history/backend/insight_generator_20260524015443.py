from backend.llm_engine import generate_response
import pandas as pd

def generate_insights(question, results):

    try:

        # --------------------------------
        # VALIDATION
        # --------------------------------

        if results is None:
            return "No results available for insights."

        # Convert results to DataFrame
        if isinstance(results, list):

            df = pd.DataFrame(results)

        elif isinstance(results, pd.DataFrame):

            df = results

        else:
            return "Unsupported result format."

        # Empty dataframe
        if df.empty:
            return "No data available for insights."

        # --------------------------------
        # LIMIT DATA
        # --------------------------------

        sample_data = df.head(10).to_string(index=False)

        # --------------------------------
        # STRICT FACTUAL PROMPT
        # --------------------------------

        prompt = f"""
You are a business analytics assistant.

Analyze ONLY the provided data.

STRICT RULES:
- DO NOT invent information.
- DO NOT assume trends.
- DO NOT calculate averages unless explicitly shown.
- DO NOT make predictions.
- ONLY mention facts directly visible in the table.
- Keep insights short.
- Use bullet points.

User Question:
{question}

Data:
{sample_data}

Provide 3 to 5 factual business insights only.
"""

        insights = generate_response(prompt)

        # --------------------------------
        # CLEAN OUTPUT
        # --------------------------------

        insights = insights.replace("```", "")
        insights = insights.replace("sql", "")

        # Remove unwanted phrases
        bad_phrases = [
            "First, let's analyze",
            "As we can see",
            "This suggests",
            "average sale",
            "consistent performer"
        ]

        for phrase in bad_phrases:
            insights = insights.replace(phrase, "")

        return insights.strip()

    except Exception as e:

        return f"Insight generation failed: {str(e)}"