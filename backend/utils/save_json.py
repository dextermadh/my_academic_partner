import json

def save_json(path, dict): 
    with open(path, 'r', encoding='utf-8') as f: 
        json.dump(dict, f, ensure_ascii=False, indent=2)