from fastapi import FastAPI, HTTPException
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import pickle
import os
import faiss
import logging

from retrieval import ask_question
from build_index import get_sources

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Initialize index and chunk store
try:
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logger.info(f"Loading index from {os.path.join(root_dir, 'rousseau_works.index')}")
    index = faiss.read_index(os.path.join(root_dir, "rousseau_works.index"))
    logger.info(f"Loading chunk store from {os.path.join(root_dir, 'rousseau_works_chunk_store.pkl')}")
    with open(os.path.join(root_dir, "rousseau_works_chunk_store.pkl"), "rb") as f:
        chunk_store = pickle.load(f)
    logger.info(f"Successfully loaded index with {index.ntotal} vectors and {len(chunk_store)} chunks")
except Exception as e:
    logger.error(f"Error loading index or chunk store: {e}")
    raise

origins = [
    "http://localhost:3000",  # Next.js default port
    "http://localhost:5173",  # Vite default port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    query: str
    chunk_count: int = 5  # Default to 5 if not specified
    mode: str = "understanding"  # Default to understanding mode

@app.get("/")
def home():
    return {"Data": "Testing"}

@app.get("/sources")
def list_sources():
    return [src["metadata"] for src in get_sources()]

@app.post("/ask")
async def ask(question: Question):
    try:
        logger.info(f"Received question: {question.query} with chunk_count: {question.chunk_count} and mode: {question.mode}")
        full_response = ask_question(question.query, index, chunk_store, mode=question.mode, top_k=question.chunk_count)
        
        # Split the response into answer and sources
        parts = full_response.split("\n\n---\n**Sources Consulted:**\n\n")
        if len(parts) != 2:
            logger.error("Unexpected response format")
            raise HTTPException(status_code=500, detail="Unexpected response format from model")
            
        answer = parts[0].strip()
        sources = [s.strip() for s in parts[1].split("\n\n") if s.strip()]
        
        logger.info("Successfully generated answer")
        return {
            "answer": answer,
            "sources": sources
        }
    except Exception as e:
        logger.error(f"Error processing question: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)