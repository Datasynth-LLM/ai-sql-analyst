from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import shutil
import pandas as pd
import os

from backend.sql_generator import generate_sql
from backend.db_manager import run_sql_query
from backend.insight_generator import generate_insights
from backend.data_loader import load_csv_to_db
from backend.chart_detector import detect_chart_type

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://datasynth-ai-sql-analyst.streamlit.app",
        "http://localhost:8501",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --------------------------------
# REQUEST MODEL
# --------------------------------

class QueryRequest(BaseModel):

    question: str
    generate_insights: bool = False

# --------------------------------
# ROOT ROUTE
# --------------------------------

@app.get("/")
def home():

    return {
        "message": "AI SQL Analyst API Running"
    }

# --------------------------------
# UPLOAD CSV
# --------------------------------

@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):

    try:

        os.makedirs(
            "data",
            exist_ok=True
        )

        save_path = os.path.join(
            "data",
            file.filename
        )

        with open(save_path, "wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        result = load_csv_to_db(
            save_path
        )

        print("\nUPLOAD RESULT:")
        print(result)

        return result

    except Exception as e:

        print("\nUPLOAD ERROR:")
        print(str(e))

        return {
            "status": "error",
            "message": str(e)
        }

# --------------------------------
# ASK AI
# --------------------------------

@app.post("/ask")
def ask_question(request: QueryRequest):

    try:

        sql_query = generate_sql(
            request.question
        )

        print("\nGENERATED SQL:")
        print(sql_query)

        results = run_sql_query(
            sql_query
        )

        if not isinstance(
            results,
            pd.DataFrame
        ):

            return {

                "error": str(results),

                "sql_query": sql_query
            }

        insights = ""

        if request.generate_insights:

            insights = generate_insights(

                request.question,

                results
            )

        chart_data = detect_chart_type(
            results
        )

        return {

            "question": request.question,

            "sql_query": sql_query,

            "results": results.to_dict(
                orient="records"
            ),

            "insights": insights,

            "chart_data": chart_data
        }

    except Exception as e:

        print("\nASK ERROR:")
        print(str(e))

        return {
            "error": str(e)
        }