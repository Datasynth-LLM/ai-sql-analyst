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
                response = requests.post(API_URL, json=payload)

                data = response.json()

                st.subheader("Generated SQL")

                st.code(data["sql_query"], language="sql")

                st.subheader("Results")

                results = data["results"]

                if results:

                    df = pd.DataFrame(results)

                    st.dataframe(
                        df,
                        use_container_width=True
                    )

                    # Optional chart
                    if "sales" in df.columns:

                        st.subheader("Sales Chart")

                        chart_df = df[["customer_name", "sales"]]

                        st.bar_chart(
                            chart_df.set_index("customer_name")
                        )

                else:
                    st.warning("No results found.")

            except Exception as e:
                st.error(f"Error: {e}")