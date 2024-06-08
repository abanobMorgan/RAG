from fastapi import FastAPI
app = FastAPI()

@app.get("/alive")
def alive():
    return {
        "message": "The RAG system is alive!"
    }