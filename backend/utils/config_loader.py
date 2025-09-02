import yaml 

def load_config(path='backend/configs/settings.yaml'): 
    with open(path, 'r') as f: 
        return yaml.safe_load(f)