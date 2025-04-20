from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from retrieval import ask_question
from build_index import get_sources

app = FastAPI()

origins = [
  "http://localhost:5173",

]

app.add_middleware(
  CORSMiddleware, 
  allow_origins = origins, 
  allow_credentials = True,
  allow_methods = ["*"],
  allow_headers = ["*"],
                   )




@app.get("/")
def home():
  return {"Data":"Testing"}

@app.get("/sources")
def list_sources():
    return [src["metadata"] for src in get_sources()]

# @app.post("/ask")
# def ask(query: str):
#   answer = ask_question(query, index, chunk_store)
#   return answer


if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port = 8000)