"""
PhilQuery - A philosophical text querying system
"""

__version__ = "0.1.0"

from .config import DATA_DIR, CACHE_PREFIX, client
from .embedder import embed_texts
from .indexing import load_index, save_index, build_faiss_index, load_and_chunk_with_metadata
from .retrieval import ask_question
