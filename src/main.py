import os
from .config import DATA_DIR, CACHE_PREFIX
from .indexing import load_index, save_index, build_faiss_index, load_and_chunk_with_metadata
from .retrieval import ask_question
from .embedder import embed_texts

def main():
    index, chunk_store = load_index(CACHE_PREFIX)

    if index is None:
        print("Building index from scratch...")
        index, chunk_store = load_index("rousseau_works")
        if index is None:
            print("No index found. Please run `build_index.py` first.")
            return
        save_index(index, chunk_store, CACHE_PREFIX)

    while True:
        question = input("Ask your political philosophy question: ")
        if question.lower() in ['q', 'quit', 'exit']:
            break
        print("\nThinking...")
        answer = ask_question(question, index, chunk_store, embed_func=embed_texts)
        print(answer)

if __name__ == "__main__":
    main()