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
            f"[{i+1}] {meta.get('source_title')} by {meta.get('author')}:\n"
            f"(Excerpt: \"{excerpt}...\")"
        )

    context = "\n\n---\n\n".join(context_parts)

    prompt = f"""You are a research assistant specializing in political philosophy.

Your goal is to synthesize Rousseau's views on the topic asked in the question, using *only* the provided context.

Instructions:
1.  Carefully read the provided context sections.
2.  Identify the main themes or categories related to the question within the context.
3.  Begin your response with a concise introductory sentence summarizing the overall topic (e.g., "Based on the provided context, Rousseau's views on [Topic] can be summarized as follows:").
4.  Organize the main body of your answer using clear thematic headings based on the categories you identified (e.g., "Theme 1:", "Theme 2:", etc.).
5.  Under each heading, summarize Rousseau's points on that theme using information *only* from the context.
6.  For the information presented under each theme, **cite the relevant source number(s)** (e.g., Source 1, Source 3). Direct quotes are optional, focus on accurate summarization and citation.
7.  Conclude with a brief overall summary paragraph synthesizing Rousseau's main position on the topic, based solely on the provided context.
8.  Format your answer clearly and analytically. Do not include any information not present in the context.
9.  If you feel you don't have enough information for the user, then explain so and do not answer the question.
10. Never quote the full source in the acutal answer, the sources are show in another place

Context:
{context}

Question: {question}
Answer:"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt},
                  {"role": "system", "content": "You are a helpful assistant specializing in political philosophy. Focus on Rousseau, cite his texts, and explain things clearly."}],
        temperature=0.2
    )
    answer = response.choices[0].message.content.strip()

    return f"{answer}\n\n---\n**Sources Consulted:**\n\n" + "\n\n".join(citations)