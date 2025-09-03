from langchain_chroma import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from .config_loader import load_config

cfg = load_config()

def load_vectorstore(): 
    embedding_fn = SentenceTransformerEmbeddings(model_name=cfg['model']['embed_model'])
    
    vectorstore = Chroma(
        persist_directory=cfg['vectorstore']['persist_directory'],
        embedding_function=embedding_fn
    )
    
    return vectorstore

def load_retriever(vectorstore): 
    retriever = vectorstore.as_retriever(search_kwargs={'k': 5})
    return retriever