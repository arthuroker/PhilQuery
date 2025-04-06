import streamlit as st
from main import load_index, ask_question

st.title("PhilQuery")

index, chunks = load_index()

if index is None or chunks is None:
    st.error("No cached index found. Please run the indexer first.")
else:
    question = st.text_input("Ask a political philosophy question:")

    if question:
        with st.spinner("Thinking..."):
            answer = ask_question(question, index, chunks)
            st.markdown("### Answer")
            st.write(answer)