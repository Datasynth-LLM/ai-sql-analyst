from fastapi import FastAPI
from pydantic import BaseModel

from backend.sql_generator import generate_sql
from backend.db_manager import run_sql_query
from backend.query_validator import validate_query
from backend.insight_generator import generate_insights

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

    # Generate SQL query
    sql_query = generate_sql(question)

    # Validate SQL safety
    is_safe = validate_query(sql_query)

    if not is_safe:

        return {
            "error": "Unsafe SQL query detected.",
            "generated_sql": sql_query
        }

    # Execute SQL query
    results = run_sql_query(sql_query)

    # Convert dataframe to dictionary
    if hasattr(results, "to_dict"):
        results = results.to_dict(orient="records")

    return {
        "question": question,
        "sql_query": sql_query,
        "results": results
    }