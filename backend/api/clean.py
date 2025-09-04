from fastapi import APIRouter, HTTPException
import sys
import os
from pathlib import Path

# Add the project root (two levels up from extract.py) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.utils.config_loader import load_config
from backend.pipelines.clean import Clean

router = APIRouter()
cfg = load_config()

@router.post('/clean/run')
def run_cleaning(): 
    """
    Run the Clean pipeline:
    1. Load raw CSVs (extracted + raw text).
    2. Apply cleaning & normalization.
    3. Save cleaned CSVs + JSONs (raw + sectioned).
    """    
    try: 
        cleaner = Clean()
        
        # step 1: save cleaned csvs
        cleaner.save_csvs_cleaned()
        
        # step 2: save cleaned jsons
        cleaner.save_jsons() 
        
        return {
            "message": "Cleaning completed successfully!",
            "outputs": {
                "cleaned_raw_csv": str(Path(cfg["paths"]["processed"]) / "cleaned_raw.csv"),
                "cleaned_sections_csv": str(Path(cfg["paths"]["processed"]) / "cleaned_sections.csv"),
                "cleaned_raw_json": str(Path(cfg["paths"]["processed"]) / "cleaned_raw.json"),
                "cleaned_sections_json": str(Path(cfg["paths"]["processed"]) / "cleaned_sections.json"),
            }            
        }
    except Exception as e: 
        return HTTPException(status_code=500, detail=f'Cleaning Failed: {e}')