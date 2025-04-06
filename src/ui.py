import streamlit as st
from main import load_index, ask_question

st.set_page_config(page_title="PhilQuery", layout="centered")

st.title("PhilQuery")
st.caption("A citation-aware political philosophy assistant by Arthur Oker")

st.markdown("""
PhilQuery is an AI-powered research assistant for political philosophy. It answers questions using **only** the text provided in its index.  
Right now, it's running on a small set of curated sources, including:

- Jean-Jacques Rousseau’s *The Social Contract* and early discourses

It uses semantic search (FAISS + sentence-transformers) to find relevant passages, then asks an LLM (via Groq) to answer based only on those chunks.  
All quotes are explicitly cited using a short excerpt from the original text.

> _"Answer the question using only the context provided."_  
""")

st.markdown("---")

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

st.markdown("---")
st.markdown("Built by [Arthur Oker](https://www.linkedin.com/in/arthuroker)")