from fastapi import FastAPI
import sys
import os

# Add the project root (two levels up from extract.py) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.api import upload, extract, clean, embeddings, agent

app = FastAPI(title="Academic RAG Chatbot API")

# Mount API routers
app.include_router(upload.router, prefix='/api', tags=['Upload'])
app.include_router(extract.router, prefix="/api", tags=["Extraction"])
app.include_router(clean.router, prefix="/api", tags=["Clean"])
app.include_router(embeddings.router, prefix="/api", tags=["Embeddings"])
app.include_router(embeddings.router, prefix="/api", tags=["Embeddings"])
app.include_router(agent.router, prefix="/api", tags=["Agent"])

@app.get("/")
def root():
    return {"message": "Academic RAG Chatbot API is running 🚀"}