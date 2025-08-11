from fastapi import FastAPI

app = FastAPI()

@app.get("/welcome")
def example():
    return {"message": "Welcome to mini-RAG"}