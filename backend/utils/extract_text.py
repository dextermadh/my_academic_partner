import fitz
import docx
from pathlib import Path
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
        