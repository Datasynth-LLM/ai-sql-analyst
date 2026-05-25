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

API_URL = "https://ai-sql-analyst-backend.onrender.com"

# --------------------------------
# SESSION STATE
# --------------------------------

if "history" not in st.session_state:
    st.session_state.history = []

if "selected_query" not in st.session_state:
    st.session_state.selected_query = ""

# --------------------------------
# SIDEBAR
# --------------------------------

st.sidebar.title("📂 Upload Multiple Datasets")

uploaded_files = st.sidebar.file_uploader(
    "Upload CSV Files",
    type=["csv"],
    accept_multiple_files=True
)

# --------------------------------
# MULTI FILE UPLOAD
# --------------------------------

if uploaded_files:

    if st.sidebar.button("Upload Datasets"):

        upload_success = []

        upload_failed = []

        for uploaded_file in uploaded_files:

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file,
                    "text/csv"
                )
            }

            with st.sidebar:

                with st.spinner(
                    f"Uploading {uploaded_file.name}..."
                ):

                    try:

                        response = requests.post(
                            f"{API_URL}/upload-csv",
                            files=files
                        )

                        data = response.json()

                        if data.get("status") == "success":

                            upload_success.append(
                                data["table_name"]
                            )

                        else:

                            upload_failed.append(
                                uploaded_file.name
                            )

                    except Exception:

                        upload_failed.append(
                            uploaded_file.name
                        )

        # --------------------------------
        # RESULTS
        # --------------------------------

        if upload_success:

            st.sidebar.success(
                f"Uploaded tables: {', '.join(upload_success)}"
            )

        if upload_failed:

            st.sidebar.error(
                f"Failed uploads: {', '.join(upload_failed)}"
            )

# --------------------------------
# HEADER
# --------------------------------

st.title("📊 AI SQL Analyst")

st.markdown("""
Professional AI-powered analytics dashboard supporting:

• Multiple Dataset Uploads  
• SQL Generation  
• KPI Analytics  
• Interactive Visualizations  
• AI Insights  
• Dynamic Table Detection  
""")

# --------------------------------
# QUICK QUERY BUTTONS
# --------------------------------

st.subheader("⚡ Quick Query Suggestions")

q1, q2, q3, q4, q5 = st.columns(5)

with q1:

    if st.button("Show Tables"):

        st.session_state.selected_query = (
            "Show available tables"
        )

with q2:

    if st.button("Top Sales"):

        st.session_state.selected_query = (
            "Show top 5 sales"
        )

with q3:

    if st.button("Top Customers"):

        st.session_state.selected_query = (
            "Show customers with highest total_spent"
        )

with q4:

    if st.button("Region Analysis"):

        st.session_state.selected_query = (
            "Show sales by region"
        )

with q5:

    if st.button("Membership Stats"):

        st.session_state.selected_query = (
            "Show average age by membership"
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

query_data = None

# --------------------------------
# GENERATE ANALYTICS
# --------------------------------

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

            try:

                response = requests.post(
                    f"{API_URL}/ask",
                    json=payload
                )

                query_data = response.json()

                if "error" not in query_data:

                    st.session_state.history.append(
                        question
                    )

            except Exception as e:

                st.error(
                    f"Backend connection failed: {e}"
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

        tab1, tab2, tab3, tab4 = st.tabs([

            "📊 Analytics",
            "📈 Visualizations",
            "🧠 AI Insights",
            "🕘 Query History"

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

            # --------------------------------
            # KPI SECTION
            # --------------------------------

            numeric_cols = df.select_dtypes(
                include="number"
            ).columns.tolist()

            col1, col2, col3, col4 = st.columns(4)

            if numeric_cols:

                metric = numeric_cols[0]

                with col1:

                    st.metric(
                        "Total",
                        round(df[metric].sum(), 2)
                    )

                with col2:

                    st.metric(
                        "Average",
                        round(df[metric].mean(), 2)
                    )

                with col3:

                    st.metric(
                        "Maximum",
                        round(df[metric].max(), 2)
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
                use_container_width=True
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
                "📈 Interactive Charts"
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

                        grouped_df = df.groupby(
                            x_col,
                            as_index=False
                        )[y_col].sum()

                        fig = None

                        if chart_type == "bar":

                            fig = px.bar(
                                grouped_df,
                                x=x_col,
                                y=y_col
                            )

                        elif chart_type == "line":

                            fig = px.line(
                                grouped_df,
                                x=x_col,
                                y=y_col
                            )

                        elif chart_type == "pie":

                            fig = px.pie(
                                grouped_df,
                                names=x_col,
                                values=y_col
                            )

                        if fig:

                            st.plotly_chart(
                                fig,
                                use_container_width=True
                            )

                except Exception as e:

                    st.error(
                        f"Chart error: {e}"
                    )

            else:

                st.info(
                    "No chart generated."
                )

        # =================================
        # TAB 3 — AI INSIGHTS
        # =================================

        with tab3:

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

elif query_data and "error" in query_data:

    st.error(
        query_data["error"]
    )