from tqdm import tqdm 
import pandas as pd
import os
import sys

# Add the project root (two levels up from extract.py) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.utils.config_loader import load_config
from backend.utils.extract_text import extract_text_from_pdf_file, extract_text_from_word_file
from backend.utils.section_splitter import split_into_section

cfg = load_config()

class Extract:
    def __init__(self, raw_dir=cfg['paths']['raw'], output_dir=cfg['paths']['extracted']):
        self.raw_dir = str(raw_dir)
        self.output_dir = str(output_dir)
        
        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

    def extract(self):
        section_records = []
        raw_records = []
        
        for file in tqdm(os.listdir(self.raw_dir)): 
            if not (file.lower().endswith('.pdf') or file.lower().endswith('.docx')): 
                continue 
            
            file_path = os.path.join(self.raw_dir, file) 
            
            # extract text depending on the file type 
            if file.lower().endswith('.pdf'): 
                raw_text = extract_text_from_pdf_file(file_path) 
            elif file.lower().endswith('.docx'):
                raw_text = extract_text_from_word_file(file_path)
            
            # save the raw version 
            raw_records.append({
                'file_name': file,
                'raw_text': raw_text
            })
            
            # save section split version 
            sections = split_into_section(raw_text)
            for section, content in sections.items(): 
                section_records.append({
                    'filename': file, 
                    'section': section,
                    'content': content
                })
            
        df_sections = pd.DataFrame(section_records)
        df_raw = pd.DataFrame(raw_records)
        
        return df_sections, df_raw
            
    def save_csvs(self):        
        # save the two dataframes(csv)
        df_sections, df_raw =  self.extract()
        df_sections.to_csv(os.path.join(self.output_dir, 'papers_extracted.csv'))
        df_raw.to_csv(os.path.join(self.output_dir, 'papers_raw.csv')) 
        # print('files saved successfully! ')

if __name__ == '__main__': 
    extract = Extract()
    extract.save_csvs()