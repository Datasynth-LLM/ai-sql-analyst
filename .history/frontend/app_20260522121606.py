import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000/ask"

# Session State
if "chat_history" not in st.session_state:

    st.session_state.chat_history = []

# Page Config
st.set_page_config(
    page_title="AI SQL Analyst",
    layout="wide"
)

# Title
st.title("📊 AI SQL Analyst")
st.markdown("Ask business questions in natural language.")

# CSV Upload Section
st.sidebar.header("Upload CSV Dataset")

uploaded_file = st.sidebar.file_uploader(
    "Choose a CSV file",
    type=["csv"]
)

# Save Uploaded File
if uploaded_file is not None:

    save_path = f"data/{uploaded_file.name}"

    with open(save_path, "wb") as f:

        f.write(uploaded_file.getbuffer())

    st.sidebar.success(
        f"Uploaded: {uploaded_file.name}"
    )

# User Input
question = st.text_input(
    "Enter your question:",
    placeholder="Example: Show top 5 highest sales"
)

# Optional Insights
generate_insights = st.checkbox(
    "Generate AI Insights (slower)",
    value=False
)

# Generate Button
if st.button("Generate Insights"):

    if question:

        with st.spinner("Processing..."):

            payload = {
                "question": question,
                "generate_insights": generate_insights
            }

            try:

                # Backend Request
                response = requests.post(
                    API_URL,
                    json=payload
                )

                data = response.json()

                # Save Chat History
                st.session_state.chat_history.append({
                    "question": question,
                    "response": data
                })

                # Error Handling
                if "error" in data:

                    st.error(data["error"])

                else:

                    # SQL Query
                    st.subheader("Generated SQL")

                    st.code(
                        data["sql_query"],
                        language="sql"
                    )

                    # AI Insights
                    if (
                        generate_insights
                        and "insights" in data
                    ):

                        st.subheader("AI Business Insights")

                        st.markdown(data["insights"])

                    # Results
                    st.subheader("Results")

                    results = data["results"]

                    if results:

                        df = pd.DataFrame(results)

                        # KPI Dashboard
                        if "sales" in df.columns:

                            total_sales = df["sales"].sum()

                            avg_sales = df["sales"].mean()

                            max_sales = df["sales"].max()

                            total_orders = len(df)

                            st.subheader("KPI Dashboard")

                            col1, col2, col3, col4 = st.columns(4)

                            col1.metric(
                                "Total Sales",
                                f"${total_sales:,.0f}"
                            )

                            col2.metric(
                                "Average Sales",
                                f"${avg_sales:,.0f}"
                            )

                            col3.metric(
                                "Highest Sale",
                                f"${max_sales:,.0f}"
                            )

                            col4.metric(
                                "Total Orders",
                                total_orders
                            )

                        # Analytics Table
                        st.subheader("Analytics Table")

                        st.dataframe(
                            df,
                            use_container_width=True
                        )

                        # Chart
                        if (
                            "customer_name" in df.columns
                            and "sales" in df.columns
                        ):

                            st.subheader("Sales Chart")

                            chart_df = df[
                                ["customer_name", "sales"]
                            ]

                            st.bar_chart(
                                chart_df.set_index(
                                    "customer_name"
                                )
                            )

                        # CSV Download
                        csv = df.to_csv(index=False)

                        st.download_button(
                            label="Download Results CSV",
                            data=csv,
                            file_name="query_results.csv",
                            mime="text/csv"
                        )

                    else:

                        st.warning("No results found.")

            except Exception as e:

                st.error(f"Error: {e}")

# Conversation History
if st.session_state.chat_history:

    st.divider()

    st.header("Conversation History")

    for chat in reversed(st.session_state.chat_history):

        st.subheader(
            f"Question: {chat['question']}"
        )

        response = chat["response"]

        if "sql_query" in response:

            st.code(
                response["sql_query"],
                language="sql"
            )