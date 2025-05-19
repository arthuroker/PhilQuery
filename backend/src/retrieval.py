# main.py
from .config import client
from .embedder import embed_texts
from .prompts import get_system_prompt
import json

def ask_question(question, index, chunk_store, mode="understanding", top_k=5):
    """
    Process a question and return a structured response with separate answer and citations.
    
    Args:
        question (str): The user's question about Rousseau
        index: The vector index for similarity search
        chunk_store: Storage containing text chunks and metadata
        mode (str): Either "understanding" or "retrieval"
        top_k (int): Number of relevant chunks to retrieve
    
    Returns:
        tuple: (answer, citations_json)
            - answer: A string containing the model's answer
            - citations_json: A JSON string of citation metadata
    """
    question_embedding = embed_texts([question])
    D, I = index.search(question_embedding, top_k)

    context_parts = []
    citations = []

    for i, idx in enumerate(I[0]):
        item = chunk_store[idx]
        meta = item['metadata']
        source_title = meta.get('source_title', 'Unknown')
        author = meta.get('author', 'Unknown')
        excerpt = item['text'][:60].strip() + "..."
        
        # Add context for the model
        context_parts.append(
            f"Source {i+1} (Title: {source_title}, Author: {author}):\n{item['text']}"
        )
        
        # Build structured citation data
        citations.append({
            "citation_id": i+1,
            "source_title": source_title,
            "author": author,
            "excerpt": excerpt,
            "full_text": item['text'],
            "url": meta.get('url', '#')
        })

    context = "\n\n---\n\n".join(context_parts)

    prompt = f"""Context:
{context}

Question: {question}
Answer:"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": get_system_prompt(mode)},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    answer = response.choices[0].message.content.strip()
    
    # Return answer and citations separately
    return answer, json.dumps(citations)