from sentence_transformers import SentenceTransformer
import faiss
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Load Groq API Key
OpenAI.api_base = "https://api.groq.com/openai/v1"
OpenAI.api_key = os.getenv("GROQ_API_KEY")

# Load embedding model
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Load and chunk text
def load_text_chunks(filepath, chunk_size = 500):
    
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

def ask_question(question, index, chunks):
    # Embed the question
    question_embedding = embedder.encode([question])

    # Search the FAISS index
    top_k = 3
    D, I = index.search(question_embedding, top_k)
    top_chunks = [chunks[i] for i in I[0]]

    # Construct context
    context = "\n\n---\n\n".join(top_chunks)

    # Prompt template
    prompt = f"""Answer the question using only the context provided. Cite anything you reference clearly by giving the first 5 words from the quote you are drawing from.

Context:
{context}

Question: {question}
Answer:"""

    # Use Groq-compatible OpenAI client
    client = OpenAI(
        api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1"
    )

    # Make the request
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content


def main():
    print("Loading and indexing philosophy text...")

    filepath = os.path.join("data", "rawls.txt")
    chunks = load_text_chunks(filepath)
    index, embeddings, chunks = build_faiss_index(chunks)

    print(f"Indexed {len(chunks)} chunks.")

    # Ask a question
    question = input("Ask your political philosophy question: ")
    answer = ask_question(question, index, chunks)
    print("\n--- Answer ---\n")
    print(answer)

if __name__ == "__main__":
    main()