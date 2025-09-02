import sys
import os
from pathlib import Path
from langchain_groq import ChatGroq

# Add the project root (two levels up from extract.py) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.utils.config_loader import load_config

cfg = load_config()

class Style: 
    def __init__(self):
        self.clean_raw_dir = Path(cfg['paths']['cleaned_raw_json'])
        self.clean_sections_dir = Path(cfg['paths']['cleaned_sections_json'])
        self.styled_dir = Path(cfg['paths']['styled'])
        self.llm = ChatGroq(model=cfg['model']['style_model'], temperature=cfg['model']['temperature'])
        
        self.styled_dir.mkdir(parents=True, exist_ok=True)
    
    