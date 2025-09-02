import sys
import os

# Add the project root (two levels up from extract.py) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.utils.chunk import chunk_text
from backend.utils.json_loader import load_json
from backend.utils.config_loader import load_config
from pathlib import Path
from tqdm import tqdm
import chromadb
from chromadb.utils import embedding_functions

cfg = load_config()

class Embeddings: 
    def __init__(self):
        self.cleaned_section_json_dir = Path(cfg['paths']['cleaned_sections_json'])
        self.vectorstore_dir = Path(cfg['paths']['vectorstore'])
        
        Path(self.vectorstore_dir).mkdir(parents=True, exist_ok=True)
    
    def generate_embeddings(self):
        cleaned_sections = load_json(self.cleaned_section_json_dir)
        
        embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=cfg['model']['embed_model']
        )
        
        chroma_client = chromadb.PersistentClient(self.vectorstore_dir)
        collection = chroma_client.get_or_create_collection(
            name=cfg['vectorstore']['collection_name'],
            embedding_function=embedding_fn
        )
        
        # generate embeddings and populate chroma 
        for fname, sections in tqdm(cleaned_sections.items()): 
            for section_name, text in sections.items(): 
                chunks = chunk_text(text)
                ids = [f'{fname}_{section_name}_{i}' for i in range(len(chunks))]
                collection.add(
                    documents=chunks, 
                    metadatas=[{'source': fname, 'section': section_name} for _ in chunks], 
                    ids=ids
                )
    
if __name__ == '__main__': 
    embeddings = Embeddings() 
    
    embeddings.generate_embeddings() 