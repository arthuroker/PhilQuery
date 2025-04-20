import os, pickle, faiss
from transformers import AutoTokenizer, logging
from embedder import embed_texts

logging.set_verbosity_error()

def load_and_chunk_with_metadata(filepath, metadata, chunk_size = 800):
    
    with open(filepath, 'r', encoding='utf-8') as f:
        words = f.read().split()

    return [{
        "text": ' '.join(words[i:i+chunk_size]),
        "metadata": metadata.copy()
    } for i in range(0, len(words), chunk_size)]

def split_to_token_chunks(text: str, tokenizer, max_len: int):
    
    token_ids = tokenizer.convert_tokens_to_ids(
        tokenizer.tokenize(text, add_special_tokens=False)
    )
    chunks = []
    for start in range(0, len(token_ids), max_len):
        sub = token_ids[start:start + max_len]
        chunks.append(tokenizer.decode(sub, clean_up_tokenization_spaces=True))

    return chunks

def section_chunker(filepath: str, metadata: dict, section_headers, chunk_size_tokens: int):

    try:
        # Use a specific model known to work or handle potential errors
        tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased", use_fast=True)
    
    except OSError:
            print("Error loading tokenizer. Ensure 'bert-base-uncased' is available or choose another.")
            return [] # Return empty list on tokenizer error


    num_special_tokens = 2

    absolute_max_len = tokenizer.model_max_length - num_special_tokens

    target_max_len = min(chunk_size_tokens, absolute_max_len)

    if target_max_len <= 0:
         print(f"Warning: Calculated target_max_len ({target_max_len}) is not positive. "
               f"Model max length ({tokenizer.model_max_length}) might be too small or "
               f"chunk_size_tokens ({chunk_size_tokens}) is too low.")

         target_max_len = min(chunk_size_tokens, 1)
         if target_max_len <=0: return [] 

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            raw = f.read()
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return []
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return []

    all_chunks = []

    for i, section in enumerate(section_headers):
        start = raw.find(section)
        if start < 0:

            print(f"Warning: Section header '{section}' not found in {filepath}")
            continue

        # Determine the end of the section
        end_marker_pos = -1
        if i + 1 < len(section_headers):

            next_section = section_headers[i+1]
            end_marker_pos = raw.find(next_section, start + len(section)) # Search after current header
            if end_marker_pos < 0:
                 end_marker_pos = len(raw)
        else:
            end_marker_pos = len(raw)


        if end_marker_pos > start :
             sec_txt = raw[start:end_marker_pos].strip()
        else:
             continue


        # Split section into paragraphs (adjust delimiter if needed)
        paragraphs = sec_txt.split("\n\n")

        for para in paragraphs:
            para = para.strip() 
            if not para: 
                continue


            tokens = tokenizer.tokenize(para, add_special_tokens=False)

            if len(tokens) <= target_max_len:

                all_chunks.append({
                    "text": para,
                    "metadata": {**metadata, "section_title": section.strip()} # Add cleaned section title
                })
            else:

                para_chunks = split_to_token_chunks(para, tokenizer, target_max_len)
                for chunk_text in para_chunks:
                    if chunk_text.strip():
                        all_chunks.append({
                            "text": chunk_text,
                            "metadata": {**metadata, "section_title": section.strip()} # Add cleaned section title
                        })

    for c in all_chunks:
        n = len(tokenizer.encode(c["text"], add_special_tokens=False))
        assert n <= target_max_len, f"Chunk too long: {n} tokens"

    return all_chunks

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