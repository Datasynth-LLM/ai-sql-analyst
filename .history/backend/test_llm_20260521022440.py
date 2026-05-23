from llm_engine import generate_response

prompt = "Write a simple SQL query to show all sales data."

response = generate_response(prompt)

print(response)