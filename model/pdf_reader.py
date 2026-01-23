import pdfplumber
import pytesseract
from pdf2image import convert_from_path
import re


# ==============================
# 1️⃣ CHECK PDF TYPE
# ==============================
def is_text_pdf(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = pdf.pages[0].extract_text()
            return bool(text and len(text.strip()) > 50)
    except:
        return False


# ==============================
# 2️⃣ EXTRACT TEXT (TEXT PDF)
# ==============================
def extract_text_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


# ==============================
# 3️⃣ EXTRACT TEXT (OCR PDF)
# ==============================
def extract_text_ocr(pdf_path):
    pages = convert_from_path(pdf_path, dpi=300)
    text = ""
    for page in pages:
        text += pytesseract.image_to_string(page, lang="eng") + "\n"
    return text


# ==============================
# 4️⃣ CLEAN & NORMALIZE TEXT
# ==============================
def clean_text(text):
    # remove encoding garbage
    text = re.sub(r'\(cid:\d+\)', '', text)

    # fix repeated OCR letters (RROOPP -> ROP)
    text = re.sub(r'([A-Z])\1+', r'\1', text)

    # fix missing space: 1.1Agricultural -> 1.1 Agricultural
    text = re.sub(r'(\d+\.\d+)([A-Za-z])', r'\1 \2', text)

    # remove vertical spaced letters (S E C T I O N)
    text = re.sub(r'(?:\b[A-Z]\b\s+){3,}', '', text)

    # normalize spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


# ==============================
# 5️⃣ HEADING DETECTOR
# ==============================
def is_heading(sentence):
    """
    Accept only real headings like:
    1.1 Agricultural Practices
    1.5 Adding Manure and Fertilisers
    """
    return bool(re.match(r'^\d+\.\d+\s+[A-Za-z][A-Za-z ]{4,}$', sentence.strip()))


# ==============================
# 6️⃣ TOPIC-WISE SPLIT
# ==============================
def extract_topics(text):
    sentences = re.split(r'(?<=\.)\s+', text)
    topics = {}
    current_topic = "INTRODUCTION"
    topics[current_topic] = ""

    for s in sentences:
        s = s.strip()
        if not s:
            continue

        if is_heading(s):
            current_topic = s
            topics[current_topic] = ""
        else:
            topics[current_topic] += s + " "

    return topics


# ==============================
# 7️⃣ MAIN EXECUTION
# ==============================
def process_pdf(pdf_path):
    """Orchestrates the PDF processing flow: Detect -> Extract -> Clean -> Split."""
    try:
        if is_text_pdf(pdf_path):
            print("✔ Text-based PDF detected")
            raw_text = extract_text_pdf(pdf_path)
        else:
            print("✔ Scanned/Broken PDF detected → OCR running")
            raw_text = extract_text_ocr(pdf_path)

        if not raw_text:
            return None, "Extraction failed: No text found."

        cleaned_text = clean_text(raw_text)
        topics = extract_topics(cleaned_text)
        
        return topics, None

    except Exception as e:
        return None, str(e)


# ==============================
# 7️⃣ MAIN EXECUTION
# ==============================
if __name__ == "__main__":
    pdf_path = "venv/material/NCERT-Books-for-class 8-Science-Chapter 1.pdf"
    
    # Run the processing pipeline
    extracted_topics, error = process_pdf(pdf_path)

    if error:
        print(f"❌ Error: {error}")
    else:
        for topic, content in extracted_topics.items():
            print(f"\n🔹 {topic}\n{content[:200]}...")  # Print first 200 chars per topic


