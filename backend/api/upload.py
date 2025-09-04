from fastapi import APIRouter, UploadFile, File, HTTPException
import sys
import os
import zipfile
import shutil
import tempfile
from pathlib import Path

# Add the project root (two levels up from extract.py) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.utils.config_loader import load_config
from backend.pipelines.upload import Upload

router = APIRouter()
cfg = load_config() 

@router.post('/upload')
async def upload_zip(file: UploadFile = File(...)): 
    '''
    upload a zip file containing pdf and word files
    extract and save them in raw directory
    '''
    if not file.filename.endswith('.zip'): 
        raise HTTPException(status_code=400, detail='Only ZIP files are ALLOWED') 
    
    # save zip temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp: 
        tmp.write(await file.read()) 
        tmp_path = Path(tmp.name) 
        
    extracted_files = []
    upload = Upload(temp_path=tmp_path) 
    
    try: 
        extracted_files = upload.save_raw_files()
    except zipfile.BadZipFile: 
        raise HTTPException(status_code=400, detail="Invalid ZIP file")
    finally: 
        tmp_path.unlink(missing_ok=True)  # clean up
        
    return {
        "message": "Files uploaded and extracted successfully",
        "extracted_files": extracted_files,
    }
    

