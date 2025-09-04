from fastapi import APIRouter, HTTPException
import sys
import os
from pathlib import Path

# Add the project root (two levels up from extract.py) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.utils.config_loader import load_config
from backend.pipelines.extract import Extract

router = APIRouter()
cfg = load_config() 

@router.post('/extract/run')
def run_extraction(): 
    '''
    Run the Extract pipeline.
    Reads PDFs/Word files from raw directory,
    saves CSVs (sections + raw text),
    and returns output file paths.
    '''
    try: 
        extract = Extract()
        extract.save_csvs()
        
        output_dir = Path(cfg['paths']['extracted'])
        return {
            "message": "Extraction completed successfully!",
            "csv_files": {
                "sections": str(output_dir / "papers_extracted.csv"),
                "raw": str(output_dir / "papers_raw.csv")
            }
        }
    except Exception as e: 
        raise HTTPException(status_code=500, detail=f'Extraction Failed: {e}')