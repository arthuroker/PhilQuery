import streamlit as st
from main import load_index, ask_question # Assuming these functions exist in main.py

# --- Page Configuration ---
# Use a more serene icon like a scroll or bamboo
st.set_page_config(
    page_title="PhilQuery 📜",
    page_icon="📜", # Scroll emoji for a classic, scholarly feel
    layout="centered",
    initial_sidebar_state="auto"
)

# --- Header ---
# Use st.title for a cleaner main heading, remove the divider argument
st.title("PhilQuery 📜")
# Slightly refined caption
st.caption("An AI assistant for exploring political philosophy texts, by Arthur Oker.")

st.divider() # Use a simple divider for separation

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
    """) # Add more sources as needed

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
try:
    # Attempt to load the index and chunks
    index, chunks = load_index(filename_prefix="rousseau_works")
    # Display a subtle success message if loaded (optional)
    # st.toast("Text index loaded successfully.", icon="✅")
except Exception as e:
    st.error(f"Failed to load the text index: {e}")
    st.warning("Ensure index files are present or run the indexer script.")
    index = None
    chunks = None

if index is None or chunks is None:
    st.error("Index data could not be loaded. Querying is disabled.")
else:
    st.markdown("### Ask Your Question") # Keep this clear and direct
    question = st.text_input(
        "Enter your political philosophy question:",
        placeholder="e.g., What is Rousseau's concept of the general will?",
        label_visibility="collapsed" # Hides the label above, cleaner look
    )

    # Use a less "primary" button for a softer look, change text slightly
    ask_button = st.button("Seek Insight") # More evocative text

    if ask_button and question:
        # Use a more thematic spinner message
        with st.spinner("Consulting the texts..."):
            try:
                answer = ask_question(question, index, chunks)
                # Use a more neutral subheader for the answer
                st.subheader("Response", divider="grey") # Changed from "Answer", use grey divider
                # Remove the border from the container for a cleaner look
                with st.container():
                    st.markdown(answer)
            except Exception as e:
                st.error(f"An error occurred while generating the response: {e}")
    elif ask_button and not question:
        st.warning("Please enter a question to explore.") # Slightly softer warning

# --- Footer ---
st.divider()
st.caption("Developed by [Arthur Oker](https://www.linkedin.com/in/arthuroker)") # Use 