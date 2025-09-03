import sys
import os
from pathlib import Path
from langchain_groq import ChatGroq
from tqdm import tqdm

# Add the project root (two levels up from extract.py) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.utils.config_loader import load_config
from backend.utils.json_loader import load_json
from backend.utils.style_text import style_text
from backend.utils.save_json import save_json
from dotenv import load_dotenv

load_dotenv()

cfg = load_config()

class Style: 
    def __init__(self):
        self.clean_raw_dir = Path(cfg['paths']['cleaned_raw_json'])
        self.clean_sections_dir = Path(cfg['paths']['cleaned_sections_json'])
        self.styled_dir = Path(cfg['paths']['styled'])
        self.llm = ChatGroq(model=cfg['model']['style_model'], temperature=cfg['model']['temperature'])
        
        self.styled_dir.mkdir(parents=True, exist_ok=True)
    
    def style_jsons(self): 
        cleaned_raw = load_json(self.clean_raw_dir)
        cleaned_sections = load_json(self.clean_sections_dir)
        
        styled_raw_dict = {}
        styled_section_dict = {}
        
        # style raw textsd
        for fname, text in tqdm(cleaned_raw.items(), desc='styling raw docs'): 
            styled_raw_dict[fname] = style_text(self.llm, text)
        
        # style section texts 
        for fname, sections in tqdm(cleaned_sections.items(), desc='styling section docs'): 
            styled_section_dict[fname] = {}
            for section, text in sections.items(): 
                styled_section_dict[fname][section] = style_text(self.llm, text) 
        
        save_json(os.path.join(self.styled_dir, 'styled_raw.json'), styled_raw_dict)
        save_json(os.path.join(self.styled_dir, 'styled_sections.json'), styled_section_dict)
        
if __name__ == '__main__': 
    style = Style() 
    
    style.style_jsons() 
        