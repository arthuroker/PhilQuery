from config import client
from embedder import embed_texts

def ask_question(question, index, chunk_store, top_k=5):

    question_embedding = embed_texts([question])

    D, I = index.search(question_embedding, top_k)

    context_parts = []
    citations = []

    for i, idx in enumerate(I[0]):
        item = chunk_store[idx]
        meta = item['metadata']
        context_parts.append(
            f"Source {i+1} (Title: {meta.get('source_title')}, Author: {meta.get('author')}):\n{item['text']}"
        )
        excerpt = item['text'][:60].strip()
        citations.append(
            f"[{i+1}] {meta.get('source_title')} by {meta.get('author')} "
            f"(Excerpt: \"{excerpt}...\")"
        )

    context = "\n\n---\n\n".join(context_parts)

    prompt = f"""You are a research assistant specializing in political philosophy.

Use *only* the provided context to answer the question. For every claim, include a short direct quote and refer to its source number.

Format your answer clearly and analytically.

Context:
{context}

Question: {question}
Answer:"""

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    answer = response.choices[0].message.content.strip()

    return f"{answer}\n\n---\n**Sources Consulted:**\n" + "\n".join(citations)