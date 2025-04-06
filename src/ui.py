import streamlit as st
from main import load_index, ask_question # Assuming these functions exist in main.py

# --- Page Configuration ---
st.set_page_config(
    page_title="PhilQuery 📖",
    page_icon="📖", # Can be an emoji or a URL
    layout="centered",
    initial_sidebar_state="auto" # Or "expanded", "collapsed"
)

# --- Header ---
st.header("PhilQuery 📖", divider='rainbow')
st.caption("A citation-aware political philosophy assistant by Arthur Oker")

# --- Introduction ---
col1, col2 = st.columns([2, 1]) # Make first column wider

with col1:
    st.markdown("""
    **Welcome to PhilQuery!**

    This is an AI-powered research assistant designed for exploring political philosophy concepts.
    It answers your questions based *strictly* on the texts indexed within its knowledge base.

    > _"Answer the question using only the context provided."_ 💬
    """)

with col2:
    st.info("**🧠 Current Knowledge Base:**")
    st.markdown("""
    * Jean-Jacques Rousseau:
        * *The Social Contract*
        * *Discourse on Inequality*
        * *Discourse on Political Economy*
        * _(Other early discourses)_
    """) # Add more sources as needed

with st.expander("⚙️ How it Works & Citations"):
    st.markdown("""
    PhilQuery uses semantic search (FAISS + sentence-transformers) to identify the most relevant passages from the indexed texts in response to your question.

    An LLM (Large Language Model accessed via Groq) then synthesizes an answer based *only* on these retrieved passages.

    Key passages used to formulate the answer are explicitly cited with a short excerpt from the original source text to ensure transparency and traceability.
    """)

st.divider() # Use st.divider for a cleaner look

# --- Main Application Logic ---
try:
    # Attempt to load the index and chunks
    index, chunks = load_index()
except Exception as e:
    st.error(f"Error loading index: {e}")
    st.warning("Please ensure the index files are present and accessible, or run the indexer script.")
    index = None # Ensure index is None if loading fails
    chunks = None

if index is None or chunks is None:
    st.error("Index data not loaded. Cannot proceed.")
    # Optionally: Add instructions or a button to trigger indexing if feasible
    # st.button("Run Indexer (Requires Setup)")
else:
    st.markdown("### 🤔 Ask Your Question")
    question = st.text_input(
        "Enter your political philosophy question:",
        placeholder="e.g., What does Rousseau say about the general will?"
    )

    ask_button = st.button("Submit Question", type="primary")

    if ask_button and question:
        with st.spinner("🧠 Thinking and searching the texts..."):
            try:
                answer = ask_question(question, index, chunks)
                st.subheader("💡 Answer", divider="grey")
                with st.container(border=True):
                    st.markdown(answer) # Use markdown to render potential formatting in the answer
            except Exception as e:
                st.error(f"An error occurred while generating the answer: {e}")
    elif ask_button and not question:
        st.warning("Please enter a question first.")

# --- Footer ---
st.divider()
st.markdown("---")
st.markdown("Built by [Arthur Oker](https://www.linkedin.com/in/arthuroker)")
