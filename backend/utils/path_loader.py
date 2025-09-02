import json 
from pathlib import Path 
from .config_loader import load_config

cfg = load_config() 

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