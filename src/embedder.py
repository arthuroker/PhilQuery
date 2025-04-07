import os
from sentence_transformers import SentenceTransformer


def embed_texts(texts):

    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    
    return embedder.encode(texts, show_progress_bar=True)