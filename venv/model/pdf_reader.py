import pdfplumber
import os

def extract_all_text(pdf_path, output_txt):
    print(f"📄 Processing: {pdf_path}")
    
    if not os.path.exists(pdf_path):
        print("❌ Error: PDF file not found!")
        return

    try:
        all_text = ""
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            print(f"📊 Found {total_pages} pages.")
            
            for i, page in enumerate(pdf.pages):
                print(f"   Extracting page {i + 1}/{total_pages}...", end='\r')
                text = page.extract_text()
                if text:
                    all_text += f"\n{text}" # Removed page markers to make topic extraction cleaner
        
        with open(output_txt, "w", encoding="utf-8") as f:
            f.write(all_text)
            
        print(f"\n✅ Success! Text saved to: {output_txt}")
        return all_text
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None

def analyze_book_content(text):
    """
    Analyzes the text to find:
    1. Main Topics (e.g. 1.1, 1.2)
    2. Sub-topics (Short headers, specific list items)
    3. Important Definitions ("is called", "is known as")
    4. Activities & Boxes
    """
    import re
    print("\n" + "="*60)
    print("📖 ADVANCED BOOK STRUCTURE ANALYSIS")
    print("="*60)
    
    lines = text.split('\n')
    structure = {
        "Topics": [],
        "SubTopics": [],
        "Definitions": [],
        "Activities": []
    }
    
    # regex patterns
    topic_pattern = r'^(\d+\.\d+)\s*(.*)'
    list_subtopic_pattern = r'^\((i+|[a-z])\)\s+([A-Z][a-z].*)'
    
    for line in lines:
        line = line.strip()
        if not line or len(line) < 3:
            continue
            
        # 1. Detect Main Topics (1.1, 1.2...)
        topic_match = re.match(topic_pattern, line)
        if topic_match:
            structure["Topics"].append(line)
            continue
            
        # 2. Detect Activities
        if line.startswith("Activity"):
            structure["Activities"].append(line)
            continue
            
        # 3. Detect Definitions (Important)
        if "is called" in line.lower() or "are called" in line.lower() or "is known as" in line.lower():
            # Clean up the definition line a bit
            structure["Definitions"].append(line)
            
        # 4. Detect Sub-topics (Short title-like lines or list items)
        # Check for (i) Preparation of soil etc.
        list_match = re.match(list_subtopic_pattern, line)
        if list_match:
            structure["SubTopics"].append(line)
        elif len(line) < 40 and line[0].isupper() and not line.endswith('.') and not any(c in line for c in '(),'):
            # Simple short header detection
            if not any(x in line for x in ["Activity", "Fig.", "Page"]):
                structure["SubTopics"].append(line)

    # PRINTING RESULTS
    print("\n📍 MAIN TOPICS:")
    for t in structure["Topics"][:15]: print(f"  ⭐ {t}")
    
    print("\n🔹 SUB-TOPICS & HEADERS:")
    for st in structure["SubTopics"][:15]: print(f"  • {st}")
    
    print("\n💡 IMPORTANT DEFINITIONS:")
    for d in structure["Definitions"][:10]:
        # Truncate long lines for cleaner output
        clean_d = d[:100] + "..." if len(d) > 100 else d
        print(f"  � {clean_d}")
        
    print("\n🧪 ACTIVITIES:")
    for a in structure["Activities"][:10]: print(f"  🔍 {a}")
    
    print("\n" + "="*60)
    return structure

if __name__ == "__main__":
    import sys
    
    # 1. Determine PDF Path
    pdf_path = None
    
    # Check command line arguments first
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        # Scan for PDF files in venv/material/ and current directory
        search_dirs = ["venv/material", "."]
        available_pdfs = []
        
        for d in search_dirs:
            if os.path.exists(d):
                for f in os.listdir(d):
                    if f.lower().endswith(".pdf"):
                        available_pdfs.append(os.path.join(d, f))
        
        if not available_pdfs:
            print("❌ No PDF files found! Please provide a path or place a PDF in the folder.")
            sys.exit(1)
            
        if len(available_pdfs) >= 1:
            pdf_path = available_pdfs[0]
            print(f"� Automatic Selection: {pdf_path}")
        else:
            print("❌ No PDF files found!")
            sys.exit(1)

    output_txt = "output.txt"
    
    # 2. Extract Text
    full_text = extract_all_text(pdf_path, output_txt)
    
    # 3. Advanced Analysis
    if full_text:
        analyze_book_content(full_text)
