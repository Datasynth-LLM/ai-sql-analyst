from backend.llm_engine import generate_response

prompt = """
You are a business analyst.

Sales by Region:

South 3200
East 2600
North 2375
West 2000

Provide business insights.
"""

response = generate_response(prompt)

print(response)