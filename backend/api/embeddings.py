from fastapi import APIRouter, HTTPException
import sys
import os

# Add the project root (two levels up from extract.py) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.pipelines.embeddings import Embeddings

router = APIRouter()

@router.post("/embed/run")
def run_embedding():
    """
    Run the Embeddings pipeline:
    1. Load cleaned JSON (sections).
    2. Generate embeddings using SentenceTransformer.
    3. Save them into a persistent ChromaDB collection.
    """
    try:
        embeddings = Embeddings()
        embeddings.generate_embeddings()

        return {
            "message": "Embeddings generated and saved to ChromaDB successfully!"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding generation failed: {str(e)}")
