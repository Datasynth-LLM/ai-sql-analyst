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
# BACKEND API URL
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

st.sidebar.title("📂 Dataset Upload")

uploaded_files = st.sidebar.file_uploader(
    "Upload CSV Files",
    type=["csv"],
    accept_multiple_files=True
)

# --------------------------------
# UPLOAD DATASETS
# --------------------------------

if uploaded_files:

    if st.sidebar.button("Upload Datasets"):

        success_count = 0

        for uploaded_file in uploaded_files:

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file,
                    "text/csv"
                )
            }

            try:

                response = requests.post(
                    f"{API_URL}/upload-csv",
                    files=files
                )

                data = response.json()

                if data.get("status") == "success":

                    success_count += 1

                    st.sidebar.success(
                        f"{uploaded_file.name} uploaded successfully!"
                    )

                else:

                    st.sidebar.error(
                        f"{uploaded_file.name}: {data.get('message')}"
                    )

            except Exception as e:

                st.sidebar.error(
                    f"{uploaded_file.name}: {str(e)}"
                )

        st.sidebar.success(
            f"{success_count} dataset(s) uploaded successfully!"
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
# QUICK QUERY SUGGESTIONS
# --------------------------------

st.subheader("⚡ Quick Query Suggestions")

q1, q2, q3, q4 = st.columns(4)

with q1:
    if st.button("Show All Tables"):
        st.session_state.selected_query = (
            "show all tables"
        )

with q2:
    if st.button("Customer Sales"):
        st.session_state.selected_query = (
            "Show customer_name and total sales"
        )

with q3:
    if st.button("Sales by Region"):
        st.session_state.selected_query = (
            "Show total sales by region"
        )

with q4:
    if st.button("Top Customers"):
        st.session_state.selected_query = (
            "Show highest spending customers"
        )

# --------------------------------
# USER QUESTION
# --------------------------------

question = st.text_input(
    "Ask your business question:",
    value=st.session_state.selected_query
)

# --------------------------------
# GENERATE ANALYTICS
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
            "generate_insights": True
        }

        try:

            with st.spinner(
                "Generating analytics..."
            ):

                response = requests.post(
                    f"{API_URL}/ask",
                    json=payload
                )

            query_data = response.json()

            st.session_state.history.append(
                question
            )

        except Exception as e:

            st.error(
                f"Backend Error: {str(e)}"
            )

# --------------------------------
# DISPLAY RESULTS
# --------------------------------

if query_data:

    if "error" in query_data:

        st.error(
            query_data["error"]
        )

    else:

        results = query_data.get(
            "results",
            []
        )

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
        # TAB 1
        # =================================

        with tab1:

            st.subheader(
                "Generated SQL Query"
            )

            st.code(
                query_data.get(
                    "sql_query",
                    ""
                ),
                language="sql"
            )

            # --------------------------------
            # DEBUG TABLE OUTPUT
            # --------------------------------

            st.subheader(
                "📋 Query Results"
            )
            

            st.dataframe(
                df,
                width="stretch"
            )

            # --------------------------------
            # KPIs
            # --------------------------------

            numeric_cols = df.select_dtypes(
                include="number"
            ).columns.tolist()

            if numeric_cols:

                metric = numeric_cols[0]

                c1, c2, c3, c4 = st.columns(4)

                with c1:
                    st.metric(
                        "Total",
                        round(
                            df[metric].sum(),
                            2
                        )
                    )

                with c2:
                    st.metric(
                        "Average",
                        round(
                            df[metric].mean(),
                            2
                        )
                    )

                with c3:
                    st.metric(
                        "Maximum",
                        round(
                            df[metric].max(),
                            2
                        )
                    )

                with c4:
                    st.metric(
                        "Rows",
                        len(df)
                    )

        # =================================
        # TAB 2
        # =================================

        with tab2:

            st.subheader(
                "📈 Visualizations"
            )

            if len(df.columns) >= 2:

                x_col = df.columns[0]
                y_col = df.columns[1]

                try:

                    fig = px.bar(
                        df,
                        x=x_col,
                        y=y_col,
                        title=f"{y_col} by {x_col}"
                    )

                    st.plotly_chart(
                        fig,
                        width="stretch"
                    )

                except Exception as e:

                    st.warning(
                        f"Chart error: {str(e)}"
                    )

        # =================================
        # TAB 3
        # =================================

        with tab3:

            st.subheader(
                "🧠 AI Insights"
            )

            insights = query_data.get(
                "insights",
                "No insights generated."
            )

            st.info(insights)

        # =================================
        # TAB 4
        # =================================

        with tab4:

            st.subheader(
                "🕘 Query History"
            )

            for item in reversed(
                st.session_state.history
            ):

                st.write(f"• {item}")