import streamlit as st
import requests
import pandas as pd

# --------------------------------
# PAGE CONFIG
# --------------------------------

st.set_page_config(
    page_title="AI SQL Analyst",
    page_icon="📊",
    layout="wide"
)

# --------------------------------
# CUSTOM CSS
# --------------------------------

st.markdown("""
<style>

.main {
    background-color: #0E1117;
    color: white;
}

h1, h2, h3 {
    color: white;
}

.stMetric {
    background-color: #1E1E1E;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #333;
}

.stDataFrame {
    border-radius: 10px;
}

.sidebar .sidebar-content {
    background-color: #111827;
}

div.stButton > button {
    width: 100%;
    border-radius: 10px;
    height: 3em;
    font-size: 16px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------
# API URL
# --------------------------------

API_URL = "http://127.0.0.1:8000"

# --------------------------------
# SESSION STATE
# --------------------------------

if "history" not in st.session_state:

    st.session_state.history = []

# --------------------------------
# SIDEBAR
# --------------------------------

st.sidebar.title("📂 Dataset Upload")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

if uploaded_file is not None:

    if st.sidebar.button("Upload Dataset"):

        files = {

            "file": (
                uploaded_file.name,
                uploaded_file,
                "text/csv"
            )
        }

        with st.sidebar:

            with st.spinner("Uploading dataset..."):

                response = requests.post(
                    f"{API_URL}/upload-csv",
                    files=files
                )

        data = response.json()

        if data.get("status") == "success":

            st.sidebar.success("Dataset uploaded successfully!")

            st.sidebar.write(f"Rows: {data['rows']}")

            st.sidebar.write(
                f"Columns: {', '.join(data['columns'])}"
            )

        else:

            st.sidebar.error(data.get("message"))

# --------------------------------
# HEADER
# --------------------------------

st.title("📊 AI SQL Analyst")

st.markdown("""
Ask business questions in natural language and get:
- SQL queries
- analytics tables
- smart charts
- AI-generated insights
""")

# --------------------------------
# USER INPUT
# --------------------------------

question = st.text_input(
    "Ask your business question:"
)

generate_insights = st.checkbox(
    "Generate AI Insights",
    value=False
)

# --------------------------------
# GENERATE BUTTON
# --------------------------------

if st.button("Generate Analytics"):

    if question.strip() == "":

        st.warning("Please enter a question.")

    else:

        payload = {

            "question": question,

            "generate_insights": generate_insights
        }

        with st.spinner("Generating analytics..."):

            response = requests.post(
                f"{API_URL}/ask",
                json=payload
            )

        data = response.json()

        # --------------------------------
        # ERROR HANDLING
        # --------------------------------

        if "error" in data:

            st.error(data["error"])

        else:

            # Save History
            st.session_state.history.append(question)

            # --------------------------------
            # SQL QUERY
            # --------------------------------

            with st.expander("Generated SQL Query"):

                st.code(
                    data["sql_query"],
                    language="sql"
                )

            # --------------------------------
            # RESULTS
            # --------------------------------

            results = data.get("results", [])

            if results:

                df = pd.DataFrame(results)

                # --------------------------------
                # KPI SECTION
                # --------------------------------

                st.subheader("📈 KPI Dashboard")

                numeric_cols = df.select_dtypes(
                    include="number"
                ).columns.tolist()

                col1, col2, col3, col4 = st.columns(4)

                if numeric_cols:

                    main_metric = numeric_cols[0]

                    with col1:

                        st.metric(
                            "Total",
                            round(df[main_metric].sum(), 2)
                        )

                    with col2:

                        st.metric(
                            "Average",
                            round(df[main_metric].mean(), 2)
                        )

                    with col3:

                        st.metric(
                            "Maximum",
                            round(df[main_metric].max(), 2)
                        )

                    with col4:

                        st.metric(
                            "Rows",
                            len(df)
                        )

                # --------------------------------
                # DATA TABLE
                # --------------------------------

                st.subheader("📋 Query Results")

                st.dataframe(
                    df,
                    use_container_width=True
                )

                # --------------------------------
                # DOWNLOAD CSV
                # --------------------------------

                csv = df.to_csv(index=False)

                st.download_button(
                    label="⬇ Download Results CSV",
                    data=csv,
                    file_name="query_results.csv",
                    mime="text/csv"
                )

                # --------------------------------
                # SMART CHARTS
                # --------------------------------

                chart_data = data.get("chart_data")

                if chart_data:

                    st.subheader("📊 Smart Visualization")

                    chart_type = chart_data["chart"]

                    x_col = chart_data["x"]

                    y_col = chart_data["y"]

                    chart_df = df[[x_col, y_col]]

                    if chart_type == "bar":

                        st.bar_chart(
                            chart_df.set_index(x_col)
                        )

                    elif chart_type == "line":

                        st.line_chart(
                            chart_df.set_index(x_col)
                        )

                # --------------------------------
                # AI INSIGHTS
                # --------------------------------

                if data.get("insights"):

                    st.subheader("🧠 AI Insights")

                    st.info(data["insights"])

            else:

                st.warning("No results found.")

# --------------------------------
# QUERY HISTORY
# --------------------------------

if st.session_state.history:

    st.sidebar.subheader("🕘 Query History")

    for item in reversed(
        st.session_state.history[-10:]
    ):

        st.sidebar.write(f"• {item}")