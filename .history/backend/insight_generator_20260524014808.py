from backend.llm_engine import generate_response
import pandas as pd

def generate_insights(question, results):

    try:

        # --------------------------------
        # VALIDATION
        # --------------------------------

        if results is None:

            return "No results available for insights."

        # Convert to dataframe if needed
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
        # USE MORE ROWS
        # --------------------------------

        # Take up to first 20 rows
        sample_data = df.head(20).to_string(index=False)

        # --------------------------------
        # PROMPT
        # --------------------------------

        prompt = f"""
You are a professional business data analyst.

Analyze the following query results and generate concise business insights.

User Question:
{question}

Query Results:
{sample_data}

Instructions:
1. Identify important trends.
2. Mention highest and lowest performers.
3. Mention anomalies if present.
4. Keep response concise and professional.
5. Use bullet points.
"""

        insights = generate_response(prompt)

        return insights.strip()

    except Exception as e:

        return f"Insight generation failed: {str(e)}"