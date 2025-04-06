from sentence_transformers import SentenceTransformer
import faiss
import os
from openai import OpenAI
from dotenv import load_dotenv
import pickle

# Load the .env file
load_dotenv()

# Load Groq API Key
OpenAI.api_base = "https://api.groq.com/openai/v1"
OpenAI.api_key = os.getenv("GROQ_API_KEY")

# Load embedding model
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Load and chunk text
def load_and_chunk_with_metadata(filepath, metadata, chunk_size=800):
    """
    Loads text from a file, chunks it, and associates metadata with each chunk.

    Args:
        filepath (str): Path to the text file.
        metadata (dict): Dictionary containing metadata (e.g., {'source_title': '...', 'author': '...'}).
        chunk_size (int): Target number of words per chunk.

    Returns:
        list: A list of dictionaries, where each dict has 'text' and 'metadata' keys.
              Returns an empty list if the file cannot be read.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            full_text = f.read()
    except FileNotFoundError:
        print(f"Warning: File not found at {filepath}. Skipping.")
        return []
    except Exception as e:
        print(f"Warning: Error reading file {filepath}: {e}")
        return []

    words = full_text.split()
    processed_chunks = []
    for i in range(0, len(words), chunk_size):
        chunk_text = ' '.join(words[i : i + chunk_size])
        # Each chunk gets a copy of the file's metadata
        # You could add chunk-specific metadata here if needed (e.g., chunk_index)
        chunk_data = {
            "text": chunk_text,
            "metadata": metadata.copy() # Use copy to avoid modifying the original dict later
        }
        processed_chunks.append(chunk_data)

    print(f"Processed {len(processed_chunks)} chunks from {metadata.get('source_title', filepath)}")
    return processed_chunks

# Embed chunks and build FAISS index
def build_faiss_index(chunk_store):
    """
    Builds a FAISS index from a list of chunk dictionaries.

    Args:
        chunk_store (list): A list of dictionaries, each with 'text' and 'metadata'.

    Returns:
        tuple: (faiss.Index, list) - The FAISS index and the original chunk_store.
               Returns (None, chunk_store) if chunk_store is empty.
    """
    if not chunk_store:
        print("Warning: chunk_store is empty. Cannot build FAISS index.")
        return None, chunk_store

    # Extract only the text for embedding
    texts_to_embed = [item['text'] for item in chunk_store]

    print(f"Generating embeddings for {len(texts_to_embed)} text chunks...")
    embeddings = embedder.encode(texts_to_embed, show_progress_bar=True) # Added progress bar

    if embeddings.ndim == 1: # Handle case of single chunk
         embeddings = embeddings.reshape(1, -1)

    if embeddings.shape[0] == 0:
        print("Warning: No embeddings were generated. Cannot build FAISS index.")
        return None, chunk_store

    dim = embeddings.shape[1]
    print(f"Building FAISS index with dimension {dim}...")
    index = faiss.IndexFlatL2(dim) # Using L2 distance
    # Add vectors in batches to potentially handle large datasets better
    index.add(embeddings)
    print(f"FAISS index built successfully with {index.ntotal} vectors.")

    # Return the index and the original chunk_store (which includes metadata)
    return index, chunk_store

def save_index(index, chunk_store, filename_prefix="cached"):
    """
    Saves the FAISS index and the chunk store (list of dicts with text and metadata).

    Args:
        index (faiss.Index): The FAISS index object.
        chunk_store (list): The list of chunk dictionaries.
        filename_prefix (str): Prefix for the saved files.
    """
    index_filename = f"{filename_prefix}.index"
    store_filename = f"{filename_prefix}_chunk_store.pkl" # Updated filename

    print(f"Saving FAISS index to {index_filename}...")
    faiss.write_index(index, index_filename)

    print(f"Saving chunk store (with metadata) to {store_filename}...")
    with open(store_filename, "wb") as f:
        pickle.dump(chunk_store, f) # Save the list of dicts

    print("Index and chunk store saved successfully.")

def load_index(filename_prefix="cached"):
    """
    Loads the FAISS index and the chunk store from files.

    Args:
        filename_prefix (str): Prefix for the files to load.

    Returns:
        tuple: (faiss.Index, list) or (None, None) if files don't exist.
    """
    index_filename = f"{filename_prefix}.index"
    store_filename = f"{filename_prefix}_chunk_store.pkl" # Updated filename

    if os.path.exists(index_filename) and os.path.exists(store_filename):
        try:
            print(f"Loading FAISS index from {index_filename}...")
            index = faiss.read_index(index_filename)
            print(f"Loading chunk store from {store_filename}...")
            with open(store_filename, "rb") as f:
                chunk_store = pickle.load(f) # Load the list of dicts
            print(f"Successfully loaded index ({index.ntotal} vectors) and chunk store ({len(chunk_store)} items).")

            # Validation
            if index.ntotal != len(chunk_store):
                print(f"Error: Index size ({index.ntotal}) and chunk store size ({len(chunk_store)}) mismatch!")
                return None, None # Indicate error on mismatch

            return index, chunk_store
        except Exception as e:
            print(f"Error loading index or chunk store: {e}")
            return None, None
    else:
        print("Cached files not found.")
        return None, None

def ask_question(question, index, chunk_store, top_k=3):
    """
    Queries the index, retrieves chunks with metadata, generates an answer using LLM,
    and includes citations.

    Args:
        question (str): The user's question.
        index (faiss.Index): The loaded FAISS index.
        chunk_store (list): The loaded list of chunk dictionaries.
        top_k (int): Number of relevant chunks to retrieve.

    Returns:
        str: The formatted answer with citations, or an error message.
    """
    if not index or not chunk_store:
         return "Error: Index or chunk store not available."

    # 1. Embed the question
    print("Embedding question...")
    question_embedding = embedder.encode([question])

    # 2. Search the FAISS index
    print(f"Searching index for top {top_k} chunks...")
    try:
         D, I = index.search(question_embedding, top_k)
    except Exception as e:
        return f"Error during FAISS search: {e}"

    # 3. Retrieve the actual items (text + metadata) using the IDs
    retrieved_indices = I[0]
    retrieved_items = []
    citations = []
    context_parts = []

    print("Retrieving and formatting context...")
    for i, doc_id in enumerate(retrieved_indices):
        if 0 <= doc_id < len(chunk_store): # Safety check
            item = chunk_store[doc_id]
            retrieved_items.append(item)
            text = item['text']
            meta = item['metadata']

            # Format context for LLM (include source info)
            source_info = f"Source {i+1} (Title: {meta.get('source_title', 'Unknown')}, Author: {meta.get('author', 'Unknown')})"
            context_parts.append(f"{source_info}:\n{text}")

            # Prepare citation string (to be added after LLM response)
            citation_text = f"[{i+1}] {meta.get('source_title', 'Unknown')} by {meta.get('author', 'Unknown')}"
            # Add chapter/page if available
            if 'chapter' in meta: citation_text += f" (Chapter: {meta.get('chapter')})"
            if 'page_number' in meta: citation_text += f" (Page: {meta.get('page_number')})"
            citation_text += f" - (Excerpt: \"{text[:60].strip()}...\")" # Add short excerpt
            citations.append(citation_text)
        else:
            print(f"Warning: Retrieved invalid ID {doc_id} from FAISS search.")

    if not context_parts:
        return "Could not find relevant passages in the indexed texts for your question."

    context = "\n\n---\n\n".join(context_parts)

    # 4. Construct the prompt for the LLM
    # (Your existing prompt is quite good, ensures focus on context and quoting)
    # We added source info into the context itself.
    prompt = f"""**Role:** You are a research assistant specializing in philosophy.
**Task:** Answer the question accurately using *only* the information present in the provided 'Context'. Do not introduce any external knowledge or interpretations. Refer to sources as 'Source 1', 'Source 2', etc., as labeled in the context.

**Instructions:**
1.  Base your entire answer strictly on the provided 'Context'.
2.  When explaining a point or concept drawn from the context, integrate a key, concise quote from the relevant passage directly into your sentence AND mention the source number (e.g., Source 1, Source 2). Structure your sentences like: "Source 1 explains that [concept] is based on [idea], stating that it '...'." or "Regarding [topic], Source 2 notes '...'."
3.  Ensure the integrated quote clearly supports the point being made and flows naturally within the sentence.
4.  Present the answer in a clear, analytical, and neutral tone.

**Context:**
{context}

**Question:** {question}

**Answer:**
"""

    # 5. Call the LLM
    print("Sending request to LLM...")
    try:
        client = OpenAI(
            api_key=os.getenv("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1"
        )
        response = client.chat.completions.create(
            model="llama3-70b-8192", # Or your preferred model
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2 # Low temp for factual recall
            # max_tokens=500 # Optional: limit response length
        )
        llm_answer = response.choices[0].message.content
        print("LLM response received.")
    except Exception as e:
        print(f"Error calling LLM: {e}")
        return f"Error generating answer from LLM: {e}"

    # 6. Combine LLM answer with formatted citations
    final_output = f"{llm_answer.strip()}\n\n---\n**Sources Consulted:**\n" + "\n".join(citations)
    return final_output



def main():
    print("Checking for cached index...")
    # Try loading first
    index, chunk_store = load_index(filename_prefix="rousseau_works") # Use a more descriptive prefix

    if index is not None and chunk_store is not None:
        print(f"Successfully loaded cached index and store.")
    else:
        print("No valid cache found or mismatch detected. Building index from scratch...")

        # --- Define Your Sources Here ---
        data_dir = "data" # Assume your texts are in a 'data' subdirectory
        sources_to_index = [
            {
                "filepath": os.path.join(data_dir, "social_contract_rousseau.txt"),
                "metadata": {"source_title": "The Social Contract", "author": "Jean-Jacques Rousseau"}
            },
        ]

        all_processed_chunks = []
        print("Loading and chunking texts...")
        for source_info in sources_to_index:
            # Use the new function to get chunks with metadata
            chunks_from_source = load_and_chunk_with_metadata(
                filepath=source_info["filepath"],
                metadata=source_info["metadata"],
                chunk_size=800 # Adjust chunk size if needed
            )
            all_processed_chunks.extend(chunks_from_source)

        if not all_processed_chunks:
            print("Error: No chunks were processed. Cannot build index.")
            return # Exit if no data

        # Build index using the combined list of dictionaries
        index, chunk_store = build_faiss_index(all_processed_chunks)

        if index is not None and chunk_store is not None:
            # Save the index and the list of dictionaries
            save_index(index, chunk_store, filename_prefix="rousseau_works")
        else:
            print("Error: Failed to build or save the index.")
            return # Exit if building failed


    # --- Querying Part (Example) ---
    if index is not None and chunk_store is not None:
        while True:
            try:
                 question = input("\nAsk your political philosophy question (or type 'quit'): ")
                 if question.lower() == 'quit':
                     break
                 if not question:
                     continue

                 print("\nThinking...")
                 answer = ask_question(question, index, chunk_store, top_k=5) # Pass chunk_store
                 print("\n--- Answer ---")
                 print(answer)
                 print("--------------")

            except EOFError: # Handle Ctrl+D
                 break
            except KeyboardInterrupt: # Handle Ctrl+C
                 break
    else:
        print("Index is not available. Cannot proceed with questions.")

    print("\nExiting PhilQuery.")


# --- Environment Setup & Entry Point ---
if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    # Check for Groq API key
    if not os.getenv("GROQ_API_KEY"):
        print("Error: GROQ_API_KEY environment variable not set.")
        print("Please create a .env file with GROQ_API_KEY=your_key")
    else:
        # Load embedding model globally (if not already done - your code has it global)
        # print("Loading embedding model...") # Moved inside build_faiss_index status message
        # embedder = SentenceTransformer('all-MiniLM-L6-v2')

        main() # Run the main logic