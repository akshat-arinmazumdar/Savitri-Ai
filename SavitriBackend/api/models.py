from django.db import models
import uuid
import os

def upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4().hex[:8]}_{instance.original_filename}"
    return os.path.join('pdfs', filename)

class PDFDocument(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='pdfs/') # We will handle naming manually if needed, or let Django do it
    uploaded_at = models.DateTimeField(auto_now_add=True)
    original_filename = models.CharField(max_length=255)

    def __str__(self):
        return self.original_filename
