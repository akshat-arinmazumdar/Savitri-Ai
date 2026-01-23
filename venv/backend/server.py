import os
import sys
import shutil
import asyncio
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Adjust paths to import from model folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'model')))

from pdf_reader import extract_all_text, analyze_book_content
from savitri_ai import run_savitri_for_topic

app = FastAPI(title="Savitri AI API")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directories
MATERIAL_DIR = os.path.join("venv", "material")
VOICES_DIR = "voices"
os.makedirs(MATERIAL_DIR, exist_ok=True)
os.makedirs(VOICES_DIR, exist_ok=True)

# Serve static audio files
app.mount("/api/voices", StaticFiles(directory=VOICES_DIR), name="voices")

class GenerateRequest(BaseModel):
    topic: str
    filename: str

@app.post("/api/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    file_path = os.path.join(MATERIAL_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"message": "Upload successful", "filename": file.filename}

@app.get("/api/topics")
async def get_topics(filename: str):
    file_path = os.path.join(MATERIAL_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    # Extract and analyze
    text = extract_all_text(file_path, "pipeline_temp.txt")
    if not text:
        raise HTTPException(status_code=500, detail="Failed to extract text from PDF")
    
    structure = analyze_book_content(text)
    topics = structure.get("Topics", []) or structure.get("SubTopics", [])
    
    # Filter noise
    filtered_topics = [t for t in topics if len(t.strip()) > 5]
    
    return {"topics": filtered_topics}

@app.post("/api/generate")
async def generate_audio(request: GenerateRequest):
    # sanitize filename if not already done by frontend
    # we reuse the logic from pipeline.py but we'll trust the frontend or re-sanitize
    success = await run_savitri_for_topic(request.topic, filename=request.filename, auto_play=False)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to generate audio")
    
    return {"message": "Generation successful", "url": f"/api/voices/{request.filename}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
