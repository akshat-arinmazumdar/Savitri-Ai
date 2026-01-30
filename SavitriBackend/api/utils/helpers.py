import re
import os
import uuid

def sanitize_filename(filename: str) -> str:
    if not filename:
        return ""
    filename = os.path.basename(filename)
    filename = re.sub(r'[^\w\s\.-]', '', filename)
    return filename.strip("._")

def make_unique_filename(filename: str) -> str:
    if not filename or filename == ".":
         filename = "document.pdf"
    unique = uuid.uuid4().hex[:8]
    return f"{unique}_{filename}"
