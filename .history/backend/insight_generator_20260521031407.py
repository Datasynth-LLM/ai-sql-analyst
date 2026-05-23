from backend.llm_engine import generate_response

def generate_insights(question, results):

    prompt = f"""
You are a business analyst AI.

Analyze the SQL query results and provide short business insights.

User Question:
{question}

Results:
{results}

Rules:
1. Keep insights short.
2. Use business language.
3. Mention trends or patterns.
4. Maximum 3 bullet points.
"""

    insights = generate_response(prompt)

    return insights