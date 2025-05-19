import os, pickle, faiss
from transformers import AutoTokenizer, logging
from .embedder import embed_texts
import logging as py_logging

# Set up logging
py_logging.basicConfig(level=py_logging.INFO)
logger = py_logging.getLogger(__name__)

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
        tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased", use_fast=True)
    except OSError:
        logger.error("Error loading tokenizer")
        return []

    num_special_tokens = 2
    absolute_max_len = tokenizer.model_max_length - num_special_tokens
    target_max_len = min(chunk_size_tokens, absolute_max_len)

    if target_max_len <= 0:
        logger.error(f"Invalid chunk size: {chunk_size_tokens} tokens")
        return []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            raw = f.read()
    except Exception as e:
        logger.error(f"Error reading {filepath}: {e}")
        return []

    all_chunks = []
    total_paragraphs = 0
    total_chunks = 0

    for i, section in enumerate(section_headers):
        start = raw.find(section)
        if start < 0:
            continue

        # Determine the end of the section
        end_marker_pos = -1
        if i + 1 < len(section_headers):
            next_section = section_headers[i+1]
            end_marker_pos = raw.find(next_section, start + len(section))
            if end_marker_pos < 0:
                end_marker_pos = len(raw)
        else:
            end_marker_pos = len(raw)

        if end_marker_pos <= start:
            continue

        sec_txt = raw[start:end_marker_pos].strip()
        paragraphs = sec_txt.split("\n\n")
        section_paragraphs = 0
        section_chunks = 0

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            # Skip if paragraph is just a header (section or chapter)
            if (para.strip() == section.strip() or 
                para.strip().startswith("CHAPTER") or 
                para.strip().startswith("BOOK") or
                len(para.split()) <= 3):  # Skip very short paragraphs that are likely headers
                continue

            tokens = tokenizer.tokenize(para, add_special_tokens=False)
            token_count = len(tokens)

            if token_count <= target_max_len:
                all_chunks.append({
                    "text": para,
                    "metadata": {**metadata, "section_title": section.strip()}
                })
                section_chunks += 1
            else:
                para_chunks = split_to_token_chunks(para, tokenizer, target_max_len)
                for chunk_text in para_chunks:
                    if chunk_text.strip():
                        all_chunks.append({
                            "text": chunk_text,
                            "metadata": {**metadata, "section_title": section.strip()}
                        })
                        section_chunks += 1

            section_paragraphs += 1

        total_paragraphs += section_paragraphs
        total_chunks += section_chunks

    logger.info(f"Created {total_chunks} chunks from {os.path.basename(filepath)}")
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