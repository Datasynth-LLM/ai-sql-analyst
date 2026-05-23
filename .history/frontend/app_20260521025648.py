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

                st.dataframe(df)

            else:
                st.warning("No results found.")

        except Exception as e:
            st.error(f"Error: {e}")