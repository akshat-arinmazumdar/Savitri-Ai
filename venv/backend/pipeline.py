import sys
import os
import asyncio
import re

# Adjust paths to import from model folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'model')))

from pdf_reader import extract_all_text, analyze_book_content
from savitri_ai import run_savitri_for_topic

def sanitize_filename(name):
    """Converts a topic name into a safe, length-limited filename."""
    # Remove special chars but keep dots and dashes
    name = re.sub(r'[^\w\s\.-]', '', name).strip()
    # Replace spaces with underscores and lowercase it
    name = name.replace(' ', '_').lower()
    # Limit length to avoid Windows path issues
    if len(name) > 60:
        name = name[:60]
    return name + ".mp3"

async def start_pipeline():
    print("\n" + "🎧 SAVITRI PLAYLIST CREATOR ".center(60, "="))
    
    # 1. Setup Paths
    pdf_dir = os.path.join("venv", "material")
    if not os.path.exists(pdf_dir):
        print(f"❌ Error: {pdf_dir} folder not found!")
        return

    available_pdfs = [f for f in os.listdir(pdf_dir) if f.lower().endswith(".pdf")]
    if not available_pdfs:
        print("❌ No PDF files found in material folder!")
        return

    selected_pdf = os.path.join(pdf_dir, available_pdfs[0])
    print(f"📄 Reading PDF: {selected_pdf}")

    # 2. Extract topics
    text = extract_all_text(selected_pdf, "pipeline_temp.txt")
    if not text: return
    
    structure = analyze_book_content(text)
    topics = structure.get("Topics", []) or structure.get("SubTopics", [])
    
    # Filter out noise (very short lines) and prepare topic data
    topics_files = []
    for t in topics:
        if len(t.strip()) > 5:
            topics_files.append({"topic": t, "file": sanitize_filename(t)})

    if not topics_files:
        print("❌ No valid topics found.")
        return

    print(f"✅ Found {len(topics_files)} lessons. Opening Playlist Menu...")

    # 3. Interactive Playlist Loop (On-Demand Generation)
    while True:
        print("\n" + "🎵 SAVITRI LESSON MENU ".center(60, "-"))
        for i, item in enumerate(topics_files, 1):
            exists = os.path.exists(os.path.join("voices", item["file"]))
            # Show if it's already generated or needs AI sync
            status = "✅ [READY]" if exists else "⏳ [NEW - NEEDS SYNC]"
            print(f"{i:>2}. {item['topic']:<50} {status}")
        
        print(f"{len(topics_files) + 1:>2}. ❌ Exit")
        
        try:
            choice = input(f"\n👉 Select a lesson (1-{len(topics_files) + 1}): ")
        except EOFError:
            break
            
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(topics_files):
                item = topics_files[idx]
                # Process on-demand: This will generate if missing, then play
                await run_savitri_for_topic(item["topic"], filename=item["file"], auto_play=True)
            elif idx == len(topics_files):
                exit_text = "Thank you for visiting Savitri. Happy learning!"
                print(f"\n🌸 {exit_text}")
                await run_savitri_for_topic("Exit", filename="exit_greeting_v3.mp3", auto_play=True, text_override=exit_text)
                break
            else:
                print("⚠️ Invalid number.")
        else:
            print("⚠️ Please enter a number.")

if __name__ == "__main__":
    try:
        asyncio.run(start_pipeline())
    except KeyboardInterrupt:
        exit_text = "Savitri Stopped. Thank you for visiting!"
        print(f"\n\n👋 {exit_text}")
        # Use a new loop for the exit message since the main one is dead
        new_loop = asyncio.new_event_loop()
        new_loop.run_until_complete(run_savitri_for_topic("Stop", filename="exit_interrupt_v3.mp3", auto_play=True, text_override=exit_text))
        sys.exit(0)
