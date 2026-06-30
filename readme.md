# 📊 AI SQL Analyst
An AI-powered Business Intelligence platform that enables users to upload CSV datasets, query them using natural language, automatically generate SQL, visualize results, and receive AI-generated business insights. The application is built with FastAPI and Streamlit, powered by Google Gemini, and deployed on Render and Streamlit Cloud.
---
## 🏗️ Architecture
```text
CSV Upload
     │
     ▼
Streamlit UI
     │
     ▼
FastAPI Backend
     │
     ▼
SQLite Database
     │
     ▼
SQL Generator
     │
     ▼
Gemini AI Insights
     │
     ▼
Dashboard + Charts
```

## Example Workflow

1. Upload a CSV dataset.
2. The application automatically creates a SQLite table.
3. Ask a business question in plain English.
4. AI generates the SQL query.
5. SQL executes against the uploaded dataset.
6. Results are displayed as tables, KPIs, and interactive charts.
7. Gemini generates business insights based on the query results.
# 🌐 Live Demo

### Frontend
https://datasynth-ai-sql-analyst.streamlit.app

### Backend API
https://ai-sql-analyst-backend.onrender.com

### GitHub Repository
https://github.com/Datasynth-LLM/ai-sql-analyst

# 🚀 Features

## ✅ AI-Powered SQL Generation
- Convert natural language into SQL queries
- Powered by Google Gemini 2.5 Flash
- Automatic SQL generation
- Dynamic schema detection
- SQLite query execution

## ✅ Interactive Analytics Dashboard
- KPI dashboards
- Smart visualizations
- Interactive Plotly charts
- Download charts as PNG
- CSV export support

## ✅ AI Business Insights
- Automated factual business insights
- Trend analysis
- Sales summaries
- Region/product/category analysis

## ✅ Smart Dashboard UX
- Quick query suggestions
- Query history
- Modern dark dashboard UI
- Interactive tabs

---

# 🛠️ Tech Stack

## Frontend
- Streamlit
- Plotly

## Backend
- FastAPI
- SQLite
- SQLAlchemy

## AI
- Google Gemini 2.5 Flash
- Google GenAI SDK

## Data Processing
- Pandas
---

## Deployment
- Streamlit Cloud
- Render

# 📂 Project Structure
```bash
ai-sql-analyst/
│
├── backend/
│   ├── main.py
│   ├── llm_engine.py
│   ├── sql_generator.py
│   ├── query_executor.py
│   ├── insights_generator.py
│   ├── chart_detector.py
│
├── frontend/
│   └── app.py
│
├── data/
│   └── sales.csv
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/Datasynth-LLM/ai-sql-analyst.git
cd ai-sql-analyst
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---
## Environment Variables

Create a .env file

GEMINI_API_KEY=YOUR_API_KEY


# ▶️ Run Backend

```bash
uvicorn backend.main:app --reload
```

Backend runs on:

```bash
http://127.0.0.1:8000
```

---

# ▶️ Run Frontend

```bash
streamlit run frontend/app.py
```

Frontend runs on:

```bash
http://localhost:8501
```

---

# 📊 Example Queries

- Show top 5 highest sales
- Show sales by region
- Show quantity by category
- Show top selling products
- Show sales trends over time

---

# 📸 Dashboard Features

- KPI cards
- Interactive Plotly charts
- AI-generated SQL
- Dataset profiling
- Business insights
- Query history
- Smart visualizations

---

# 👨‍💻 Author

Developed by Datasynth-LLM

GitHub:
https://github.com/Datasynth-LLM

---

# ⭐ If you found this project useful, consider starring the repository.
