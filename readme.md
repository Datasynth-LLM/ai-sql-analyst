# 📊 AI SQL Analyst

An AI-powered Business Intelligence dashboard that converts natural language questions into SQL queries, executes them on uploaded datasets, and generates analytics, visualizations, KPI dashboards, and AI-powered business insights.

---

# 🚀 Features

## ✅ AI-Powered SQL Generation
- Convert natural language into SQL queries
- Powered by local LLMs using Ollama
- SQLite-compatible query generation

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

## ✅ Dataset Profiling
- Missing value analysis
- Data type inspection
- Numeric & categorical column detection
- Unique value analysis
- Dataset preview dashboard

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

## AI / LLM
- Ollama
- TinyLlama

## Data Processing
- Pandas

---

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
git clone https://github.com/YOUR_USERNAME/ai-sql-analyst.git
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

# 🤖 Setup Ollama

Install Ollama:

- https://ollama.com

Pull TinyLlama model:

```bash
ollama pull tinyllama
```

Start Ollama server:

```bash
ollama serve
```

---

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

# 🎯 Future Enhancements

- Multi-database support
- Authentication system
- Saved dashboards
- Cloud deployment
- Chat-style analytics assistant
- Advanced LLM integrations

---

# 👨‍💻 Author

Developed by Avish

GitHub:
https://github.com/Datasynth-LLM

---

# ⭐ If you found this project useful, consider starring the repository.