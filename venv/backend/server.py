import os
import sys

# Safe encoding fix for Windows
try:
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

import re
import uuid
import shutil
import asyncio
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

#=======================PATH FIX===============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "..", "model" )
sys.path.append(MODEL_DIR)

from pdf_reader import extract_all_text, analyze_book_content
from savitri_ai import run_savitri_for_topic
#==============================================================

app = FastAPI(title="Savitri AI API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#=========================Directories==========================
MATERIAL_DIR = os.path.join(BASE_DIR, "..", "material")
VOICES_DIR = os.path.join(BASE_DIR, "voices")

os.makedirs(MATERIAL_DIR, exist_ok=True)
os.makedirs(VOICES_DIR, exist_ok=True)

app.mount("/api/voices", StaticFiles(directory=VOICES_DIR), name="voices")
#========================Mount Static Files======================

class GenerateRequest(BaseModel):
    topic: str
    filename: str

#===================ADDED SECURITY FUNCTION===================
def sanitize_filename(filename: str) -> str:

    if not filename:
        return ""

    filename = os.path.basename(filename)

    filename = re.sub(r'[^\w\s\.-]', '', filename)

    return filename.strip("._")


def make_unique_filename(filename: str) -> str:
    # Ensure filename is not empty or just dots
    if not filename or filename == ".":
         filename = "document.pdf"
         
    unique = uuid.uuid4().hex[:8]
    return f"{unique}_{filename}"

#============================================================
    




@app.post("/api/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename missing")

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid PDF MIME type")

    MAX_SIZE = 50 * 1024 * 1024  # 50MB
    content = await file.read(MAX_SIZE + 1)

    if len(content) > MAX_SIZE:
        raise HTTPException(status_code=400, detail="File too large")

    if not content.startswith(b"%PDF-"):
        raise HTTPException(status_code=400, detail="Invalid PDF file")

    safe_name = sanitize_filename(file.filename)
    if not safe_name:
        raise HTTPException(status_code=400, detail="Invalid filename")
    
    unique_name = make_unique_filename(safe_name)
    file_path = os.path.join(MATERIAL_DIR, unique_name)

    with open(file_path, "wb") as f:
        f.write(content)

    return {"message": "Upload successful", "filename": unique_name}





#===================FIX: SECURE FILENAME======================

@app.get("/api/topics")
async def get_topics(filename: str):
    safe_filename = sanitize_filename(filename)
    if not safe_filename:
        raise HTTPException(status_code=400, detail="Invalid filename")

    file_path = os.path.join(MATERIAL_DIR, safe_filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    temp_file = f"temp_{uuid.uuid4().hex[:8]}.txt"
   
#================================================================

    try:
        
        text = await asyncio.to_thread(extract_all_text, file_path, temp_file)

        if not text:
            raise HTTPException(status_code=500, detail="Failed to extract text from PDF")

        structure = await asyncio.to_thread(analyze_book_content, text)

        structure = structure or {}  
        
        topics = structure.get("Topics", [])
        subtopics = structure.get("SubTopics", [])
        combined_topics = topics + subtopics
        
        filtered_topics = []
        seen = set()

        for t in combined_topics:
            cleaned = t.strip()
            # Only include short, topic-like items (not full sentences)
            if 5 < len(cleaned) < 100 and cleaned not in seen:
                filtered_topics.append(cleaned)
                seen.add(cleaned)
            
        print(f"DEBUG: Found {len(filtered_topics)} filtered topics for dashboard.")
        return {"topics": filtered_topics}

   
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

#===========================================================================================

@app.post("/api/generate")
async def generate_audio(request: GenerateRequest):
    #================================FIX SUCURE FILENAME===================================

    filename = request.filename
    if not filename.lower().endswith("mp3"):
        filename += ".mp3"

    safe_filename = sanitize_filename(filename)
    if not safe_filename:
        raise HTTPException(status_code=400, detail="Invalid filename")

    output_path = os.path.join(VOICES_DIR, safe_filename)

    #================================================================================

    try:
        success = await run_savitri_for_topic(
            request.topic,
            filename=output_path,
            auto_play=False
        )
    
        if not success:
            raise HTTPException(status_code=500, detail="Failed to generate audio")

        return {
            "message": "Generation successful", 
            "url": f"/api/voices/{request.filename}"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail= f"Generation failed: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
