from fastapi import FastAPI
from pydantic import BaseModel

from sql_generator import generate_sql
from db_manager import run_sql_query

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

@app.get("/")
def home():
    return {
        "message": "AI SQL Analyst API is running"
    }

@app.post("/ask")
def ask_question(request: QueryRequest):

    question = request.question

    # Generate SQL
    sql_query = generate_sql(question)

    # Execute query
    results = run_sql_query(sql_query)

    # Convert dataframe to dictionary
    if hasattr(results, "to_dict"):
        results = results.to_dict(orient="records")

    return {
        "question": question,
        "sql_query": sql_query,
        "results": results
    }