from fastapi import FastAPI

app = FastAPI()

@app.post("/ask")
def ask_question:
  