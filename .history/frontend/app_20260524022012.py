import streamlit as st
import requests
import pandas as pd
import plotly.express as px

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
    border-radius: 12px;
    border: 1px solid #333;
}

div.stButton > button {
    width: 100%;
    border-radius: 10px;
    height: 3em;
    font-size: 15px;
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

if "dataset_info" not in st.session_state:
    st.session_state.dataset_info = {}

if "selected_query" not in st.session_state:
    st.session_state.selected_query = ""

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

            st.session_state.dataset_info = data

            st.sidebar.success(
                "Dataset uploaded successfully!"
            )

            st.sidebar.write(
                f"Rows: {data['rows']}"
            )

            st.sidebar.write(
                f"Columns: {', '.join(data['columns'])}"
            )

        else:

            st.sidebar.error(
                data.get("message")
            )

# --------------------------------
# HEADER
# --------------------------------

st.title("📊 AI SQL Analyst")

st.markdown("""
Ask business questions in natural language and generate:

• SQL Queries  
• Analytics Tables  
• Interactive Visualizations  
• KPI Dashboards  
• AI-Powered Business Insights  
""")

# --------------------------------
# QUICK QUERY SUGGESTIONS
# --------------------------------

st.subheader("⚡ Quick Query Suggestions")

q1, q2, q3, q4, q5 = st.columns(5)

with q1:
    if st.button("Top Sales"):
        st.session_state.selected_query = (
            "Show top 5 highest sales"
        )

with q2:
    if st.button("Sales by Region"):
        st.session_state.selected_query = (
            "Show sales by region"
        )

with q3:
    if st.button("Top Products"):
        st.session_state.selected_query = (
            "Show top selling products"
        )

with q4:
    if st.button("Revenue Trends"):
        st.session_state.selected_query = (
            "Show sales by order date"
        )

with q5:
    if st.button("Category Analysis"):
        st.session_state.selected_query = (
            "Show quantity by category"
        )

# --------------------------------
# USER INPUT
# --------------------------------

question = st.text_input(
    "Ask your business question:",
    value=st.session_state.selected_query
)

generate_insights = st.checkbox(
    "Generate AI Insights",
    value=True
)

# --------------------------------
# PROCESS QUERY
# --------------------------------

query_data = None

if st.button("Generate Analytics"):

    if question.strip() == "":

        st.warning(
            "Please enter a question."
        )

    else:

        payload = {
            "question": question,
            "generate_insights": generate_insights
        }

        with st.spinner(
            "Generating analytics..."
        ):

            response = requests.post(
                f"{API_URL}/ask",
                json=payload
            )

        query_data = response.json()

        if "error" not in query_data:

            st.session_state.history.append(
                question
            )

# --------------------------------
# DISPLAY RESULTS
# --------------------------------

if query_data and "error" not in query_data:

    results = query_data.get(
        "results",
        []
    )

    if results:

        df = pd.DataFrame(results)

        # --------------------------------
        # TABS
        # --------------------------------

        tab1, tab2, tab3, tab4, tab5 = st.tabs([

            "📊 Analytics",
            "📈 Visualizations",
            "🧠 AI Insights",
            "🕘 Query History",
            "📂 Dataset Info"

        ])

        # =================================
        # TAB 1 — ANALYTICS
        # =================================

        with tab1:

            st.subheader(
                "Generated SQL Query"
            )

            st.code(
                query_data["sql_query"],
                language="sql"
            )

            st.subheader(
                "📈 KPI Dashboard"
            )

            numeric_cols = df.select_dtypes(
                include="number"
            ).columns.tolist()

            numeric_cols = [

                col for col in numeric_cols

                if "id" not in col.lower()
            ]

            main_metric = None

            for metric in [
                "sales",
                "revenue",
                "profit",
                "quantity"
            ]:

                if metric in numeric_cols:

                    main_metric = metric
                    break

            if main_metric is None and numeric_cols:

                main_metric = numeric_cols[0]

            col1, col2, col3, col4 = st.columns(4)

            if main_metric:

                with col1:
                    st.metric(
                        "Total",
                        round(
                            df[main_metric].sum(),
                            2
                        )
                    )

                with col2:
                    st.metric(
                        "Average",
                        round(
                            df[main_metric].mean(),
                            2
                        )
                    )

                with col3:
                    st.metric(
                        "Maximum",
                        round(
                            df[main_metric].max(),
                            2
                        )
                    )

                with col4:
                    st.metric(
                        "Rows",
                        len(df)
                    )

            st.subheader(
                "📋 Query Results"
            )

            st.dataframe(
                df,
                width="stretch"
            )

            csv = df.to_csv(
                index=False
            )

            st.download_button(
                label="⬇ Download Results CSV",
                data=csv,
                file_name="query_results.csv",
                mime="text/csv"
            )

        # =================================
        # TAB 2 — VISUALIZATIONS
        # =================================

        with tab2:

            st.subheader(
                "📊 Interactive Visualizations"
            )

            chart_data = query_data.get(
                "chart_data"
            )

            if chart_data:

                try:

                    chart_type = chart_data["chart"]

                    x_col = chart_data["x"]

                    y_col = chart_data["y"]

                    if (
                        x_col in df.columns
                        and
                        y_col in df.columns
                    ):

                        chart_df = df[
                            [x_col, y_col]
                        ].copy()

                        chart_df = chart_df.dropna()

                        # GROUPING
                        if chart_type in [
                            "bar",
                            "line",
                            "pie"
                        ]:

                            chart_df = chart_df.groupby(
                                x_col,
                                as_index=False
                            )[y_col].sum()

                        # BAR CHART
                        if chart_type == "bar":

                            fig = px.bar(
                                chart_df,
                                x=x_col,
                                y=y_col,
                                title=f"{y_col} by {x_col}"
                            )

                            st.plotly_chart(
                                fig,
                                width="stretch"
                            )

                        # LINE CHART
                        elif chart_type == "line":

                            fig = px.line(
                                chart_df,
                                x=x_col,
                                y=y_col,
                                markers=True,
                                title=f"{y_col} Trend"
                            )

                            st.plotly_chart(
                                fig,
                                width="stretch"
                            )

                        # PIE CHART
                        elif chart_type == "pie":

                            fig = px.pie(
                                chart_df,
                                names=x_col,
                                values=y_col,
                                title=f"{y_col} Distribution"
                            )

                            st.plotly_chart(
                                fig,
                                width="stretch"
                            )

                        # SCATTER CHART
                        elif chart_type == "scatter":

                            fig = px.scatter(
                                chart_df,
                                x=x_col,
                                y=y_col,
                                title=f"{x_col} vs {y_col}"
                            )

                            st.plotly_chart(
                                fig,
                                width="stretch"
                            )

                        st.success(
                            f"Chart Type: {chart_type.upper()}"
                        )

                except Exception as e:

                    st.error(
                        f"Visualization error: {e}"
                    )

            else:

                st.info(
                    "No chart available."
                )

        # =================================
        # TAB 3 — AI INSIGHTS
        # =================================

        with tab3:

            st.subheader(
                "🧠 Business Insights"
            )

            insights = query_data.get(
                "insights"
            )

            if insights:

                st.info(insights)

            else:

                st.warning(
                    "No insights generated."
                )

        # =================================
        # TAB 4 — QUERY HISTORY
        # =================================

        with tab4:

            st.subheader(
                "🕘 Previous Queries"
            )

            if st.session_state.history:

                for i, item in enumerate(

                    reversed(
                        st.session_state.history
                    ),

                    start=1
                ):

                    st.write(
                        f"{i}. {item}"
                    )

            else:

                st.info(
                    "No query history yet."
                )

        # =================================
        # TAB 5 — DATASET INFO
        # =================================

        with tab5:

            st.subheader(
                "📂 Dataset Information"
            )

            dataset_info = st.session_state.dataset_info

            if dataset_info:

                st.write(
                    f"Rows: {dataset_info.get('rows')}"
                )

                st.write(
                    f"Table Name: {dataset_info.get('table_name')}"
                )

                st.write("Columns:")

                for col in dataset_info.get(
                    "columns",
                    []
                ):

                    st.write(f"• {col}")

            else:

                st.info(
                    "No dataset uploaded yet."
                )

elif query_data and "error" in query_data:

    st.error(
        query_data["error"]
    )