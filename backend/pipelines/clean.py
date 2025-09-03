from pathlib import Path
import pandas as pd
import sys
import os

# Add the project root (two levels up from extract.py) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.utils.config_loader import load_config
from backend.utils.preprocess_utils import apply_clean
import os
import json

cfg = load_config()

class Clean:
    def __init__(self, raw_extracted_csv=Path(cfg['paths']['raw_extracted_csv']), raw_raw_csv=Path(cfg['paths']['raw_raw_csv']), processed_dir=Path(cfg['paths']['processed'])):
        self.raw_extracted_csv = raw_extracted_csv
        self.raw_raw_csv = raw_raw_csv
        self.processed_dir = processed_dir
        
    def load_csvs(self): 
        df_raw = pd.read_csv(self.raw_raw_csv)
        df_sections = pd.read_csv(self.raw_extracted_csv) 
        
        return df_raw, df_sections 
    
    def apply_clean_df(self):         
        df_raw, df_sections = self.load_csvs() 
        
        # apply cleaning to raw documents
        df_raw, df_sections = apply_clean(df_raw, df_sections)
        
        return df_raw, df_sections
    
    def save_csvs_cleaned(self):
        df_raw, df_sections = self.apply_clean_df() 
        
        # save the files
        df_raw.to_csv(os.path.join(self.processed_dir, 'cleaned_raw.csv'), index=False)
        df_sections.to_csv(os.path.join(self.processed_dir, 'cleaned_sections.csv'), index=False)
        
    def load_csvs_cleaned(self, cleaned_raw_csv, cleaned_sections_csv): 
        df_cleaned_raw = pd.read_csv(cleaned_raw_csv)
        df_cleaned_sections = pd.read_csv(cleaned_sections_csv)
        
        return df_cleaned_raw, df_cleaned_sections
        
    def save_jsons(self): 
        df_cleaned_raw, df_cleaned_sections = self.load_csvs_cleaned(os.path.join(self.processed_dir, 'cleaned_raw.csv'), os.path.join(self.processed_dir, 'cleaned_sections.csv'))
        
        # raw texts to json
        raw_dict = {row['file_name']: row['cleaned_text'] for _, row in df_cleaned_raw.iterrows()} 
        
        # werite raw jsons
        with open(os.path.join(self.processed_dir, 'cleaned_raw.json'), 'w', encoding='utf-8') as f: 
            json.dump(raw_dict, f, ensure_ascii=False, indent=2) 
            
        # sectioned texts json
        section_dict = {}
        
        for _, row in df_cleaned_sections.iterrows(): 
            fname = row['filename']
            section_dict.setdefault(fname, {})
            section_dict[fname][row['section']] = row['cleaned_content']

        with open(os.path.join(self.processed_dir, 'cleaned_sections.json'), 'w', encoding='utf-8') as f: 
            json.dump(section_dict, f, ensure_ascii=False, indent=2)     
    
if __name__ == '__main__': 
    clean = Clean() 
    
    clean.save_csvs_cleaned()
    
    clean.save_jsons() 
    
    
    
    
    
    

        
        
    