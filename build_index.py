# build_index.py

import os
from dotenv import load_dotenv
from src.indexing import load_and_chunk_with_metadata, build_faiss_index, save_index

# Load .env in case you want to test locally
load_dotenv()

def main():
    print("📚 Building index for Rousseau...")

    data_dir = "data"
    sources = [
        {
            "filepath": os.path.join(data_dir, "social_contract_rousseau.txt"),
            "metadata": {
                "source_title": "The Social Contract",
                "author": "Jean-Jacques Rousseau"
            }
        },
    ]

    all_chunks = []
    for source in sources:
        chunks = load_and_chunk_with_metadata(
            filepath=source["filepath"],
            metadata=source["metadata"],
            chunk_size=800
        )
        all_chunks.extend(chunks)

    if not all_chunks:
        print("❌ No chunks found. Exiting.")
        return

    index, chunk_store = build_faiss_index(all_chunks)

    if index is not None and chunk_store is not None:
        save_index(index, chunk_store, filename_prefix="rousseau_works")
        print(f"✅ Saved index and metadata for {len(chunk_store)} chunks.")
    else:
        print("❌ Failed to build index.")

if __name__ == "__main__":
    main()