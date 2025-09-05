from langchain_openai import ChatOpenAI
from openai import OpenAI
from backend.utils.config_loader import load_config

cfg = load_config()

def setup_llm(model_type: str):
    llm = ChatOpenAI(
        model=cfg['model-local'][str(model_type)],
        base_url=cfg['model-local']['api_base'],   # http://localhost:1234/v1
        api_key=cfg['model-local']['api_key'],     # "lm-studio"
        temperature=cfg['model-local']['temperature'],
        top_p=0.9
    )
    # else:
    #     # Default (Groq, OpenAI, etc.)
    #     from langchain_groq import ChatGroq
    #     llm = ChatGroq(
    #         model=cfg['model'][str(model_type)],
    #         temperature=cfg['model']['temperature']
    #     )
    return llm