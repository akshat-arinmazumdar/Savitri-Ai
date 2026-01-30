from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os
import json
import asyncio
from .models import PDFDocument
from .utils.pdf_reader import extract_all_text, analyze_book_content
from .utils.savitri_ai import run_savitri_for_topic
from .utils.helpers import sanitize_filename, make_unique_filename

# Helper for async views compatibility if needed, or just use async def with django 3.1+
# Django 5.0 supports async views natively for function based views.

@csrf_exempt
def upload_pdf(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    if 'file' not in request.FILES:
        return JsonResponse({'detail': 'No file part'}, status=400)

    file = request.FILES['file']
    if not file.name.lower().endswith('.pdf'):
         return JsonResponse({'detail': 'Only PDF files allowed'}, status=400)

    # Sanitize and Save
    safe_name = sanitize_filename(file.name)
    original_filename = safe_name
    
    # Create DB Entry (and let it handle file path or do manual)
    # We will save manually to match previous logic logic or use model
    # Model uses upload_to='pdfs/', so it saves to MEDIA_ROOT/pdfs/
    
    doc = PDFDocument.objects.create(original_filename=file.name, file=file, title=file.name)
    
    # We return the filename that the frontend expects?
    # Frontend expects "filename": unique_name
    # The file is saved at doc.file.path
    
    return JsonResponse({'message': 'Upload successful', 'filename': os.path.basename(doc.file.name)})

import traceback

@csrf_exempt
def get_topics(request):
    filename = request.GET.get('filename')
    print(f"DEBUG: get_topics called for: {filename}")
    
    if not filename:
        return JsonResponse({'detail': 'Filename missing'}, status=400)

    # In legacy server, filename was just the unique name.
    # Here, it is likely "pdfs/unique_filename.pdf" or just "unique_filename.pdf" depending on Model.
    
    # We need to find the file path.
    # We can rely on MEDIA_ROOT.
    
    # Try finding in pdfs/ first (default upload location)
    file_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', os.path.basename(filename)) 
    
    print(f"DEBUG: Requested filename: {filename}")
    print(f"DEBUG: Checking path: {file_path}")
    
    if not os.path.exists(file_path):
        # Fallback: check directly in MEDIA_ROOT
        file_path = os.path.join(settings.MEDIA_ROOT, filename)
        print(f"DEBUG: Fallback path: {file_path}")
        
    if not os.path.exists(file_path):
         print("DEBUG: File NOT FOUND")
         return JsonResponse({'detail': 'File not found'}, status=404)
         
    temp_file = os.path.join(settings.MEDIA_ROOT, f"temp_{os.path.basename(filename)}.txt")
    print(f"DEBUG: Temp file: {temp_file}")
    
    try:
        text = extract_all_text(file_path, temp_file)
        if not text:
             return JsonResponse({'detail': 'Failed to extract text'}, status=500)
             
        structure = analyze_book_content(text)
        structure = structure or {}
        
        topics = structure.get("Topics", [])
        subtopics = structure.get("SubTopics", [])
        combined = topics + subtopics
        
        filtered = []
        seen = set()
        for t in combined:
            cleaned = t.strip()
            if 5 < len(cleaned) < 100 and cleaned not in seen:
                filtered.append(cleaned)
                seen.add(cleaned)
                
        return JsonResponse({'topics': filtered})
        
    except Exception as e:
        print("ERROR IN GET_TOPICS:")
        traceback.print_exc()
        return JsonResponse({'detail': str(e)}, status=500)
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

@csrf_exempt
async def generate_audio(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
        
    try:
        data = json.loads(request.body)
        topic = data.get('topic')
        filename = data.get('filename') # This is the "safe_filename" usually from frontend state
        
        if not topic or not filename:
             return JsonResponse({'detail': 'Missing topic or filename'}, status=400)
             
        # Ensure mp3
        if not filename.lower().endswith("mp3"):
            filename += ".mp3"
            
        safe_name = sanitize_filename(filename)
        
        # Audio Dir
        voices_dir = os.path.join(settings.MEDIA_ROOT, 'voices')
        os.makedirs(voices_dir, exist_ok=True)
        
        output_path = os.path.join(voices_dir, safe_name)
        
        # Run AI (Async)
        success = await run_savitri_for_topic(topic, filename=output_path, auto_play=False)
        
        if not success:
            return JsonResponse({'detail': 'Failed to generate audio'}, status=500)
            
        return JsonResponse({
            'message': 'Generation successful',
            'url': f"{settings.MEDIA_URL}voices/{safe_name}"
        })

    except Exception as e:
        return JsonResponse({'detail': str(e)}, status=500)
