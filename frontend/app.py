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

if "dataset_uploaded" not in st.session_state:
    st.session_state.dataset_uploaded = False

if "query_data" not in st.session_state:
    st.session_state.query_data = None

# --------------------------------
# CSS
# --------------------------------

st.markdown("""
<style>

.stMetric{
    background:#1E1E1E;
    padding:15px;
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

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
# UPLOAD
# --------------------------------

if uploaded_files:

    if st.sidebar.button("Upload Datasets"):

        success_count = 0

        with st.spinner("Uploading datasets..."):

            for uploaded_file in uploaded_files:

                try:

                    files = {
                        "file": (
                            uploaded_file.name,
                            uploaded_file,
                            "text/csv"
                        )
                    }

                    response = requests.post(
                        f"{API_URL}/upload-csv",
                        files=files,
                        timeout=120
                    )
                    
                    response.raise_for_status()
                    
                    data = response.json()
                       
                    if data.get("status") == "success":

                        success_count += 1

                        st.sidebar.success(
                            f"✅ {uploaded_file.name}"
                        )

                    else:

                        st.sidebar.error(
                            f"❌ {uploaded_file.name}"
                        )

                except Exception as e:

                    st.sidebar.error(
                        str(e)
                    )

        if success_count > 0:

            st.session_state.dataset_uploaded = True

            st.sidebar.success(
                f"{success_count} dataset(s) uploaded successfully"
            )

# --------------------------------
# HEADER
# --------------------------------

st.title("📊 AI SQL Analyst")

st.markdown("""
AI Powered Analytics Dashboard

• CSV Upload
• SQL Generation
• KPI Analytics
• Visualizations
• AI Insights
""")

# --------------------------------
# QUICK BUTTONS
# --------------------------------

st.subheader("⚡ Quick Query Suggestions")

c1, c2, c3, c4 = st.columns(4)

with c1:

    if st.button("Show All Tables"):

        st.session_state.selected_query = (
            "show all tables"
        )

with c2:

    if st.button("Customer Sales"):

        st.session_state.selected_query = (
            "show customer sales"
        )

with c3:

    if st.button("Sales by Region"):

        st.session_state.selected_query = (
            "show total sales by region"
        )

with c4:

    if st.button("Top Customers"):

        st.session_state.selected_query = (
            "show highest spending customers"
        )

# --------------------------------
# QUESTION
# --------------------------------

question = st.text_input(
    "Ask your business question",
    value=st.session_state.selected_query
)

# --------------------------------
# GENERATE
# --------------------------------

if st.button("Generate Analytics"):

    if question.strip() == "":

        st.warning(
            "Please enter a question"
        )

    else:

        try:

            payload = {
                "question": question,
                "generate_insights": True
            }

            with st.spinner(
                "Generating analytics..."
            ):

                response = requests.post(
                    f"{API_URL}/ask",
                    json=payload,
                    timeout=120
                )
                response.raise_for_status()
                

            st.session_state.query_data = (
                response.json()
            )

            st.session_state.history.append(
                question
            )

        except Exception as e:

            st.error(
                f"Backend Error: {str(e)}"
            )

# --------------------------------
# RESULTS
# --------------------------------

query_data = st.session_state.query_data

if query_data:

    if "error" in query_data:

        st.error(
            query_data["error"]
        )

    else:

        df = pd.DataFrame(
            query_data.get(
                "results",
                []
            )
        )

        tab1, tab2, tab3, tab4 = st.tabs(
            [
                "📊 Analytics",
                "📈 Visualizations",
                "🧠 AI Insights",
                "🕘 History"
            ]
        )

        # -------------------------
        # ANALYTICS
        # -------------------------

        with tab1:

            st.subheader(
                "Generated SQL"
            )

            st.code(
                query_data.get(
                    "sql_query",
                    ""
                ),
                language="sql"
            )

            st.subheader(
                "Results"
            )

            st.dataframe(
                df,
                width=True
            )

            numeric_cols = (
                df.select_dtypes(
                    include="number"
                ).columns.tolist()
            )

            if numeric_cols:

                metric = numeric_cols[0]

                m1, m2, m3, m4 = st.columns(4)

                m1.metric(
                    "Total",
                    round(
                        df[metric].sum(),
                        2
                    )
                )

                m2.metric(
                    "Average",
                    round(
                        df[metric].mean(),
                        2
                    )
                )

                m3.metric(
                    "Maximum",
                    round(
                        df[metric].max(),
                        2
                    )
                )

                m4.metric(
                    "Rows",
                    len(df)
                )

        # -------------------------
        # VISUALIZATION
        # -------------------------

        with tab2:

            if len(df.columns) >= 2:

                try:

                    fig = px.bar(
                        df,
                        x=df.columns[0],
                        y=df.columns[1]
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

                except Exception as e:

                    st.warning(
                        str(e)
                    )

        # -------------------------
        # INSIGHTS
        # -------------------------

        with tab3:

            st.markdown(
                query_data.get(
                    "insights",
                    "No insights"
                )
            )

        # -------------------------
        # HISTORY
        # -------------------------

        with tab4:

            for item in reversed(
                st.session_state.history
            ):

                st.write(
                    f"• {item}"
                )
