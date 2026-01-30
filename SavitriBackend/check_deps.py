import sys
print(f"Python Executable: {sys.executable}")
try:
    import pdfplumber
    print("✅ pdfplumber imported")
except ImportError as e:
    print(f"❌ pdfplumber FAILED: {e}")

try:
    import edge_tts
    print("✅ edge_tts imported")
except ImportError as e:
    print(f"❌ edge_tts FAILED: {e}")

try:
    import requests
    print("✅ requests imported")
except ImportError as e:
    print(f"❌ requests FAILED: {e}")

try:
    from api.utils.pdf_reader import extract_all_text
    print("✅ api.utils.pdf_reader imported")
except Exception as e:
    print(f"❌ api.utils.pdf_reader FAILED: {e}")
