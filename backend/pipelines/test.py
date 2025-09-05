from langchain_openai import ChatOpenAI
import sys
import os
# Add the project root (two levels up from extract.py) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from backend.utils.setup_llm import setup_llm



try:
    llm = setup_llm('chat_model')
    response = llm.invoke("What is the capital of France?")
    print(response.content)
except Exception as e:
    print(f"Error: {str(e)}")