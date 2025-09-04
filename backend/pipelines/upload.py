from pathlib import Path
import sys
import os
import zipfile
import shutil
import tempfile

# Add the project root (two levels up from extract.py) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.utils.config_loader import load_config

cfg = load_config()


class Upload: 
    def __init__(self, temp_path):
        self.raw_dir = Path(cfg['paths']['raw'])
        self.temp_path = temp_path
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        
    def save_raw_files(self): 
        extracted_files = []
        
        with zipfile.ZipFile(self.temp_path, 'r') as zip_ref: 
            for member in zip_ref.namelist(): 
                if member.endswith('/'):  # skip folders
                    continue
                
                file_bytes = zip_ref.read(member)
                filename = Path(member).name
                
                save_path  = self.raw_dir / filename
                with open(save_path, 'wb') as f: 
                    f.write(file_bytes)
                extracted_files.append(str(filename))
        
        return extracted_files
        