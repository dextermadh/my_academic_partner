from langchain_groq import ChatGroq
from .config_loader import load_config

cfg = load_config()

def setup_llm(model_type): 
    llm = ChatGroq(
        model=cfg['model'][str(model_type)],
        temperature=0.3
    )
    
    return llm
