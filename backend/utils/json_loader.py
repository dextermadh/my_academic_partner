import json 
from pathlib import Path

def load_json(path): 
    with open(Path(path), 'r', encoding='utf-8') as f: 
        json_file = json.load(f)
        return json_file