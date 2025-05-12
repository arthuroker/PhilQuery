import streamlit as st

# This must be the first Streamlit command
st.set_page_config(
    page_title="PhilQuery 📜",
    page_icon="📜",
    layout="centered",
    initial_sidebar_state="auto"
)

import sys
import os

src_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(src_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.retrieval import ask_question
from src.indexing import load_index
from src.embedder import embed_texts

@st.cache_resource
def get_index():
    return load_index(prefix="rousseau_works")

index, chunks = get_index()

# --- Header ---
st.title("PhilQuery 📜")

st.divider()

# --- Introduction & Knowledge Base ---
col1, col2 = st.columns([3, 2]) # Slightly adjust column ratio if desired

with col1:
    # Keep the core message, maybe slightly rephrase for serenity
    st.markdown("""
    **Welcome.**

    PhilQuery provides answers grounded *exclusively* in the indexed philosophical texts.
    Engage with core ideas directly from the source.

    > *"Seek understanding from the text itself."*
    """) # Slightly rephrased quote concept

with col2:
    # Use a subheader for the knowledge base - cleaner than st.info
    st.subheader("Source Texts") # More direct title
    # Using subtle bullet points (hyphens or asterisks)
    st.markdown("""
    - **Jean-Jacques Rousseau:**
        - *The Social Contract*
        - *Discourse on Inequality*
        - *Discourse on Political Economy*
        - *Other early discourses*
    """) 

# --- How it Works Expander ---
# Use a more neutral icon or symbol if desired, gear is okay for 'how it works'
with st.expander("Understanding the Process ⚙️"): # Slightly softer title
    st.markdown("""
    PhilQuery employs semantic search to find relevant passages within the texts for your query.

    An AI then synthesizes an answer based *solely* on these findings.

    Key source passages are cited with excerpts for transparency and direct reference.
    """)

st.divider()

# --- Main Application Logic ---

if index is None or chunks is None:
    st.error("Index data could not be loaded. Querying is disabled.")
else:
    st.markdown("### Ask Your Question")
    
    # Add slider for number of chunks
    num_chunks = st.slider(
        "Number of source passages to consider",
        min_value=1,
        max_value=10,
        value=5,
        help="Adjust how many relevant passages from the texts should be used to generate the answer"
    )
    
    with st.expander("ℹ️ Understanding the number of passages"):
        st.markdown("""
        **Fewer passages (1-3):**
        - ✅ More focused and concise answers
        - ✅ Better for specific, targeted questions
        - ❌ May miss relevant context from other parts of the text
        - ❌ Could lead to incomplete or biased responses

        **More passages (7-10):**
        - ✅ Broader context and more comprehensive answers
            - ✅ Better for complex topics that span multiple sections
            - ✅ More likely to capture nuanced relationships between ideas
        - ❌ May include less relevant information
        - ❌ Responses might be longer and more verbose
        - ❌ Could potentially dilute the most relevant insights

        **Medium (4-6):**
        - ✅ Good balance between focus and comprehensiveness
        - ✅ Suitable for most general questions
        - ✅ Default setting for optimal results
        """)

    question = st.text_input(
        "Enter your political philosophy question:",
        placeholder="e.g., What is Rousseau's concept of the general will?",
        label_visibility="collapsed",
        key="question_input"
    )

    col1, col2 = st.columns([1, 5])
    with col1:
        ask_button = st.button("Seek Insight")
    with col2:
        st.write("")  # Empty space for alignment

    # Check for both button click and Enter key
    if (ask_button or (question and st.session_state.question_input != "")) and question:
        with st.spinner("Consulting the texts..."):
            try:
                answer = ask_question(question, index, chunks, top_k=num_chunks)
                st.subheader("Response", divider="grey")
                with st.container():
                    st.markdown(answer)
            except Exception as e:
                st.error(f"An error occurred while generating the response: {e}")
    elif ask_button and not question:
        st.warning("Please enter a question to explore.")

# --- Footer ---
st.divider()
st.caption("Developed by [Arthur Oker](https://www.linkedin.com/in/arthuroker)")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 