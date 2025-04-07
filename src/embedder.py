from sentence_transformers import SentenceTransformer

embedder = SentenceTransformer("all-MiniLM-L6-v2")

def embed_texts(texts):
    return embedder.encode(texts, show_progress_bar=True)