from backend.llm_engine import generate_response
import pandas as pd

def generate_insights(question, results):

    try:

        # --------------------------------
        # VALIDATION
        # --------------------------------

        if results is None:
            return "No results available for insights."

        # Convert to DataFrame
        if isinstance(results, list):

            df = pd.DataFrame(results)

        elif isinstance(results, pd.DataFrame):

            df = results

        else:
            return "Unsupported result format."

        # Empty DataFrame
        if df.empty:
            return "No data available for insights."

        # --------------------------------
        # LIMIT DATA
        # --------------------------------

        sample_data = df.head(10).to_string(index=False)

        # --------------------------------
        # STRICT PROMPT
        # --------------------------------

        prompt = f"""
You are an expert business analyst.

Analyze the business data below and provide REAL insights.

IMPORTANT RULES:
- DO NOT repeat instructions.
- DO NOT describe columns.
- DO NOT explain what you are doing.
- ONLY provide business insights.
- Mention actual values from the data.
- Use concise bullet points.

User Question:
{question}

Business Data:
{sample_data}

Generate professional business insights now.
"""

        insights = generate_response(prompt)

        # --------------------------------
        # CLEAN RESPONSE
        # --------------------------------

        insights = insights.replace("```", "")
        insights = insights.replace("sql", "")

        return insights.strip()

    except Exception as e:

        return f"Insight generation failed: {str(e)}"