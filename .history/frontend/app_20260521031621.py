import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000/ask"

st.set_page_config(
    page_title="AI SQL Analyst",
    layout="wide"
)

st.title("📊 AI SQL Analyst")
st.markdown("Ask business questions in natural language.")

# User input
question = st.text_input(
    "Enter your question:",
    placeholder="Example: Show top 5 highest sales"
)

if st.button("Generate Insights"):

    if question:

        with st.spinner("Generating insights..."):

            payload = {
                "question": question
            }

            try:

                response = requests.post(
                    API_URL,
                    json=payload
                )

                data = response.json()

                # Error handling
                if "error" in data:

                    st.error(data["error"])

                    if "generated_sql" in data:
                        st.code(
                            data["generated_sql"],
                            language="sql"
                        )

                else:

                    # Generated SQL
                    st.subheader("Generated SQL")

                    st.code(
                        data["sql_query"],
                        language="sql"
                    )

                    # AI Insights
                    st.subheader("AI Business Insights")

                    st.markdown(data["insights"])

                    # Results Table
                    st.subheader("Results")

                    results = data["results"]

                    if results:

                        df = pd.DataFrame(results)

                        st.dataframe(
                            df,
                            use_container_width=True
                        )

                        # Sales chart
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

                        # Download CSV
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