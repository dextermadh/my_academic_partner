import json 
from pathlib import Path
import fitz
import docx
from .config_loader import load_config

cfg = load_config()

def extract_text_from_pdf_file(file_path): 
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"Files not found: {file_path}")
    
    # function to extract texts from pdf 
    doc = fitz.open(file_path)
    text_pages = []
    
    for page_num in range(len(doc)): 
        text = doc[page_num].get_text('text')
        text_pages.append(text)
    
    return '\n'.join(text_pages) 
    
    
    
def extract_text_from_word_file(file_path):   
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"Files not found: {file_path}")
      
    # function to extract texts from word files 
    doc = docx.Document(file_path)
    return '\n'.join([para.text for para in doc.paragraphs if para.text.strip()])
        


def load_json(path): 
    with open(Path(path), 'r', encoding='utf-8') as f: 
        json_file = json.load(f)
        return json_file
    
def save_json(path, dict): 
    with open(path, 'r', encoding='utf-8') as f: 
        json.dump(dict, f, ensure_ascii=False, indent=2)
        

def load_style_json(file_key: str): 
    '''
    Load style jsons (styled_raw.json or styled_sections.json)
    based on the paths defined in settings.yaml
    
    Args: 
        file_key (str): 'styled_raw' or 'styled_section'
        
    Returns:
        dict: Parsed JSON content
    '''
    
    file_path = Path(cfg['paths'][file_key])
    
    if not file_path.exists(): 
        raise FileNotFoundError(f'Style file not found: {file_path}')
    
    with open(file_path, 'r', encoding='utf-8'): 
        return json.load() 