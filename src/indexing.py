import os, pickle, faiss
from .embedder import embed_texts

def load_and_chunk_with_metadata(filepath, metadata, chunk_size=800):
    with open(filepath, 'r', encoding='utf-8') as f:
        words = f.read().split()

    return [{
        "text": ' '.join(words[i:i+chunk_size]),
        "metadata": metadata.copy()
    } for i in range(0, len(words), chunk_size)]

def build_faiss_index(chunks):
    texts = [c['text'] for c in chunks]
    embeddings = embed_texts(texts)
    if embeddings.ndim == 1:
        embeddings = embeddings.reshape(1, -1)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return index, chunks

def save_index(index, chunks, filename_prefix="cached"):
    faiss.write_index(index, f"{filename_prefix}.index")
    with open(f"{filename_prefix}_chunk_store.pkl", "wb") as f:
        pickle.dump(chunks, f)

def load_index(prefix):
    try:
        index = faiss.read_index(f"{prefix}.index")
        with open(f"{prefix}_chunk_store.pkl", "rb") as f:
            chunks = pickle.load(f)
        if index.ntotal != len(chunks):
            return None, None
        return index, chunks
    except Exception as e:
      print(f"Error loading index: {e}")
      return None, None