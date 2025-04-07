import os

from sentence_transformers import SentenceTransformer

# Only load model if in embedding mode (i.e., during index building)
embedder = None
if os.getenv("PHILQUERY_MODE") == "embed":
    embedder = SentenceTransformer("all-MiniLM-L6-v2")

def embed_texts(texts):
    if embedder is None:
        raise RuntimeError("Embedder is not available. You should not call embed_texts on the cloud.")
    return embedder.encode(texts, show_progress_bar=True)