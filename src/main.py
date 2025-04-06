from sentence_transformers import SentenceTransformer
import faiss
import os
from openai import OpenAI
from dotenv import load_dotenv
import pickle
import streamlit as st

# Load the .env file
load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY", st.secrets.get("GROQ_API_KEY", "")),
    base_url="https://api.groq.com/openai/v1"
)

# Load Groq API Key
OpenAI.api_base = "https://api.groq.com/openai/v1"
OpenAI.api_key = os.getenv("GROQ_API_KEY")

# Load embedding model
embedder = None
if os.getenv("PHILQUERY_MODE") == "embed":
    from sentence_transformers import SentenceTransformer
    embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Load and chunk text
def load_text_chunks(filepath, chunk_size = 800):
    
    with open(filepath, 'r', encoding = 'utf-8') as f:
        full_text = f.read()

    # Simple chunking by words
    words = full_text.split()
    chunks = [
        ' '.join(words[i: i + chunk_size])
        for i in range(0, len(words), chunk_size)
    ]
    return chunks

# Embed chunks and build FAISS index
def build_faiss_index(chunks):
    embeddings = embedder.encode(chunks)
    dim = embeddings[0].shape[0]

    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    return index, embeddings, chunks

def save_index(index, embeddings, chunks, filename_prefix="cached"):
    faiss.write_index(index, f"{filename_prefix}.index")
    with open(f"{filename_prefix}_chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)

def load_index(filename_prefix="cached"):
    if os.path.exists(f"{filename_prefix}.index") and os.path.exists(f"{filename_prefix}_chunks.pkl"):
        index = faiss.read_index(f"{filename_prefix}.index")
        with open(f"{filename_prefix}_chunks.pkl", "rb") as f:
            chunks = pickle.load(f)
        return index, chunks
    return None, None

def ask_question(question, index, chunks):
    
    try:
        # Try using local embedder first
        question_embedding = embedder.encode([question])
    except Exception:
        # Fallback: use Groq to embed the question
        response = client.embeddings.create(
            model="nomic-embed-text",
            input=[question]
        )
        question_embedding = [response.data[0].embedding]

    # Search the FAISS index
    top_k = 3
    D, I = index.search(question_embedding, top_k)
    top_chunks = [chunks[i] for i in I[0]]

    # Construct context
    context = "\n\n---\n\n".join(top_chunks)

    # Prompt template
    prompt = f"""**Role:** You are a research assistant specializing in philosophy.
**Task:** Answer the question accurately using *only* the information present in the provided 'Context'. Do not introduce any external knowledge or interpretations.

**Instructions:**
1.  Base your entire answer strictly on the provided 'Context'.
2.  When explaining a point or concept drawn from the context, integrate a key, concise quote from the relevant passage directly into your sentence to provide evidence and grounding. Structure your sentences like: "The context explains that [concept] is based on [idea], stating that it '...'." or "Regarding [topic], the text notes '...'."
3.  Ensure the integrated quote clearly supports the point being made and flows naturally within the sentence.
4.  Present the answer in a clear, analytical, and neutral tone.

**Context:**
{context}

**Question:** {question}

**Answer:**
"""

    # Make the request
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content


def main():
    # Check if we're in embedding mode
    if os.getenv("PHILQUERY_MODE") == "embed":
        print("Running in embedding mode...")

        filepath = os.path.join("data", "social_contract_rousseau.txt")
        chunks = load_text_chunks(filepath)
        index, embeddings, chunks = build_faiss_index(chunks)
        save_index(index, embeddings, chunks)

        print(f"Indexed and cached {len(chunks)} chunks.")
        return 

    # Otherwise, run in normal query mode
    print("Checking for cached index...")

    index, chunks = load_index()

    if index is not None and chunks is not None:
        print(f"Loaded {len(chunks)} chunks from cache.")
    else:
        print("No cache found. Building index from scratch...")

        filepath = os.path.join("data", "social_contract_rousseau.txt")
        chunks = load_text_chunks(filepath)
        index, embeddings, chunks = build_faiss_index(chunks)
        save_index(index, embeddings, chunks)
        print(f"Indexed and cached {len(chunks)} chunks.")

    # Ask a question
    question = input("Ask your political philosophy question: ")
    answer = ask_question(question, index, chunks)
    print("\n--- Answer ---\n")
    print(answer)

if __name__ == "__main__":
    main()