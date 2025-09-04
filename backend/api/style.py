from fastapi import APIRouter, HTTPException
import sys
import os

# Add the project root (two levels up from extract.py) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.pipelines.style import Style

router = APIRouter()

@router.post("/style/run")
def run_styling():
    """
    Run the Style pipeline:
    1. Load cleaned raw + section JSONs.
    2. Apply stylistic transformation using ChatGroq.
    3. Save styled_raw.json and styled_sections.json.
    """
    try:
        styler = Style()
        styler.style_jsons()
        return {
            "message": "Styling completed successfully!",
            "output_files": ["styled_raw.json", "styled_sections.json"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Styling failed: {str(e)}")
