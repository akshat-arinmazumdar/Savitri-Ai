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
    1. Main Topics (e.g. 1.1, 1.2, or "1. Introduction")
    2. Sub-topics (Short headers, specific list items)
    3. Important Definitions ("is called", "is known as")
    4. Activities & Boxes
    """
    import re
    print("\n" + "="*60)
    print("📖 ADVANCED BOOK STRUCTURE ANALYSIS")
    print("="*60)
    
    # Pre-process text: Join lines that are likely part of the same header
    raw_lines = text.split('\n')
    lines = []
    current_line = ""
    
    # regex patterns for detection
    topic_pattern = r'^(\d+(\.\d+)?)\s*(.*)'
    activity_marker = "Activity"
    
    for rl in raw_lines:
        rl = rl.strip()
        if not rl:
            if current_line:
                lines.append(current_line)
                current_line = ""
            continue
            
        # Ignore page markers and simple numeric footers
        if rl.startswith("--- Page") or (rl.isdigit() and len(rl) < 4) or "SCIENCE" in rl:
            continue
            
        # Check if rl starts a new topic/activity
        is_new_start = re.match(topic_pattern, rl) or rl.startswith(activity_marker)
        
        if current_line:
            # If current_line doesn't end in punctuation AND next line doesn't start a new topic
            if not current_line[-1] in ".!?:;-" and not is_new_start and (rl[0].islower() or len(rl) < 40):
                current_line += " " + rl
            else:
                lines.append(current_line)
                current_line = rl
        else:
            current_line = rl
    if current_line:
        lines.append(current_line)

    print(f"DEBUG: Processed into {len(lines)} semantic blocks.")

    structure = {
        "Topics": [],
        "SubTopics": [],
        "Definitions": [],
        "Activities": []
    }
    
    # regex patterns - relaxed
    topic_pattern = r'^(\d+(\.\d+)?)\s*(.*)' # 1.1 or 1 Introduction
    list_subtopic_pattern = r'^\((i+|[a-z]|[0-9])\)\s*(.*)'
    
    for line in lines:
        line = line.strip()
        if len(line) < 5:
            continue
            
        # 1. Detect Main Topics
        topic_match = re.match(topic_pattern, line)
        if topic_match:
            # Clean up: "1.1Agricultural Practices" -> "1.1 Agricultural Practices"
            num = topic_match.group(1)
            content = topic_match.group(3).strip()
            if content:
                structure["Topics"].append(f"{num} {content}")
                continue
            
        # 2. Detect Activities
        if line.startswith("Activity"):
            structure["Activities"].append(line)
            continue
            
        # 3. Detect Definitions
        if any(phrase in line.lower() for phrase in ["is called", "are called", "is known as", "defined as"]):
            # Find the term being defined (often at the end or start)
            structure["Definitions"].append(line)
            
        # 4. Detect Sub-topics (Short title-like lines or list items)
        list_match = re.match(list_subtopic_pattern, line)
        if list_match:
            structure["SubTopics"].append(line)
        elif 5 < len(line) < 60 and line[0].isupper() and not line.endswith('.') and not any(c in line for c in '(),'):
            if not any(x in line for x in ["Activity", "Fig.", "Tab.", "Page"]):
                # Additional check: doesn't look like a normal sentence start
                if len(line.split()) < 10:
                    structure["SubTopics"].append(line)

    # PRINTING RESULTS
    print("\n📍 EXTRACTED ITEMS (COMBINED):")
    all_items = structure["Topics"] + structure["SubTopics"] + structure["Definitions"] + structure["Activities"]
    for item in all_items[:20]: print(f"  ⭐ {item}")
    
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
