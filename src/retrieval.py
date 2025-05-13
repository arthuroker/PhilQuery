from config import client
from embedder import embed_texts

def get_system_prompt(mode):
    if mode == "understanding":
        return """You are a research assistant specializing in political philosophy.

Your goal is to synthesize Rousseau's views on the topic asked in the question, using *only* the provided context.

Instructions:
1.  Carefully read the provided context sections.
2.  Identify the main themes or categories related to the question within the context.
3.  Begin your response with a concise introductory sentence summarizing the overall topic.
4.  Organize the main body of your answer using clear thematic headings based on the categories you identified.
5.  For each theme:
    - Provide a detailed explanation of Rousseau's position (4-6 sentences)
    - Include specific examples or arguments from the text
    - Explain how this theme relates to the broader question
    - Connect it to other relevant themes when appropriate
    - **Cite the relevant source number(s)** for each point
6.  Under each heading, ensure your analysis is thorough and well-supported by the context.
7.  Conclude with a comprehensive summary paragraph that:
    - Synthesizes the main themes
    - Highlights key relationships between ideas
    - Shows how they form a coherent position
8.  Format your answer clearly and analytically. Do not include any information not present in the context.
9.  If you feel you don't have enough information, explain so and do not answer the question.
10. Never quote the full source in the actual answer, the sources are shown in another place."""
    else:  # retrieval mode
        return """You are a research assistant specializing in political philosophy.

Your goal is to find and present specific passages from Rousseau's works that directly address the user's query.

Instructions:
1.  Start directly with the passages, no introduction
2.  For each relevant passage:
    - Create a descriptive title that captures the main topic
    - Write a 2-3 sentence summary on a new line
    - Include a brief, relevant snippet on a new line
3.  Format each passage exactly as shown in the example
4.  Do not add any relevance explanations or source citations
5.  If no relevant passages are found, simply state "No directly relevant passages found."
6.  Keep summaries concise and focused on the content
7.  Never quote the full source, the sources are shown separately

Example format:

**The Distinction Between Public and Private Economy**

Summary: Rousseau explains how public economy differs from private economy, emphasizing that the former must be guided by different principles than the latter. He argues that public economy requires a broader perspective that considers the general will and common good.

Quote: "Public economy is to the state what private economy is to the family. The state and the family are the only two societies that exist by nature."

**The Role of Government in Economic Affairs**

Summary: The passage outlines the government's responsibility in managing public resources and ensuring economic justice. It emphasizes that the state must act as a guardian of the common good rather than pursuing private interests.

Quote: "The government is not the master of the people but their servant; it exists to protect their rights and promote their welfare."
"""

def ask_question(question, index, chunk_store, mode="understanding", top_k=5):
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

    return f"{answer}\n\n---\n**Sources Consulted:**\n\n" + "\n\n".join(citations)