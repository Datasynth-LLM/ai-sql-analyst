from fastapi import FastAPI
from pydantic import BaseModel

from backend.sql_generator import generate_sql
from backend.db_manager import run_sql_query
from backend.insight_generator import generate_insights

app = FastAPI()

# Request Model
class QueryRequest(BaseModel):

    question: str
    generate_insights: bool = False

# Root Route
@app.get("/")
def home():

    return {
        "message": "AI SQL Analyst API Running"
    }

# Ask Route
@app.post("/ask")
def ask_question(request: QueryRequest):

    try:

        # Generate SQL
        sql_query = generate_sql(
            request.question
        )

        # Execute SQL
        results = run_sql_query(sql_query)

        insights = ""

        # Optional AI Insights
        if request.generate_insights:

            insights = generate_insights(results)

        return {

            "question": request.question,

            "sql_query": sql_query,

            "results": results.to_dict(
                orient="records"
            ),

            "insights": insights
        }

    except Exception as e:

        return {
            "error": str(e)
        }