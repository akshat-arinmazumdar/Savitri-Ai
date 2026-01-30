import os
import requests
import asyncio
import edge_tts
import re
import time
from playsound import playsound

# ================= CONFIG =================
API_KEY = os.environ.get("HF_TOKEN", "") # Set your token as an environment variable
MODEL_AI = "meta-llama/Llama-3.2-1B-Instruct"
AI_ROUTER_URL = "https://router.huggingface.co/v1/chat/completions"

# Audio Settings
SPEECH_RATE = "+15%" 
OUTPUT_DIR = "voices"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ================= AI FUNCTIONS =================

def get_academic_summary(topic):
    """Gets a comprehensive academic summary in English only."""
    prompt = f"""
You are an expert academic lecturer.
Topic: {topic}
Task: Provide a professional, clear, and comprehensive explanation of this topic.
Language: Strictly English only. Do not use any other languages or scripts.
Format: 
- Definition
- Key Points
- Conclusion
"""
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {"model": MODEL_AI, "messages": [{"role": "user", "content": prompt}], "max_tokens": 600}

    try:
        response = requests.post(AI_ROUTER_URL, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content'].strip()
        return f"❌ AI Error {response.status_code}"
    except Exception as e:
        return f"❌ AI Exception: {str(e)}"

# ================= VOICE FUNCTIONS =================

def clean_text(text):
    """Removes markdown symbols like **, #, etc. for smooth speech."""
    text = re.sub(r'\*\*|#|\[|\]', '', text)
    return text.strip()

async def run_savitri_for_topic(topic, filename=None, auto_play=True, text_override=None):
    """Modular function to process a single topic or direct text using Neerja."""
    # Versioning filename to bypass old male-voice cache
    if not filename:
        filename = "temp_speech_v2.mp3"
    elif not filename.endswith("_v2.mp3"):
        filename = filename.replace(".mp3", "_v2.mp3")
    
    out_path = os.path.abspath(os.path.join(OUTPUT_DIR, filename))
    
    # 1. Generation Phase (Cache Check)
    if not os.path.exists(out_path):
        if text_override:
            content = text_override
        else:
            print(f"⏳ Generating Summary for: {topic}...")
            content = get_academic_summary(topic)
            if "❌" in content:
                print(f"⚠️ AI Failure: {content}. Using fallback summary.")
                content = f"The topic is {topic}. Unfortunately, the AI summarization service is currently unavailable. Please check your API key or connection."
                
            print(f"\n{content}\n")
            
        print(f"🎙️ Creating Audio (Voice: Neerja, Female) -> {filename}")
        
        try:
            # Clean text for smoother speech
            text_to_speak = clean_text(content).replace(".", ",").replace("।", ",")
            communicate = edge_tts.Communicate(text_to_speak, "en-IN-NeerjaNeural", rate=SPEECH_RATE)
            await communicate.save(out_path)
            print(f"✨ Generation Complete: {filename}")
        except Exception as e:
            import traceback
            error_msg = f"⚠️ Generation Error: {str(e)}\n{traceback.format_exc()}"
            print(error_msg)
            with open("api_debug.log", "a", encoding="utf-8") as f:
                f.write(f"\n--- ERROR ---\n{error_msg}\n")
            return False
    else:
        print(f"📁 Playing from Cached File: {filename}")

    # 2. Playback Phase
    if auto_play:
        try:
            if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
                print("🔊 Playing Audio...")
                time.sleep(0.5) # Windows file system grace period
                playsound(out_path)
                print("✅ Playback Finished.")
            else:
                print(f"⚠️ Audio file error: {filename} is missing or corrupted.")
                return False
        except Exception as e:
            print(f"⚠️ Playback Error: {e}")
            print("💡 TIP: Check your system volume or if another app is using the audio device.")
            return False
    
    return True

# ================= MAIN =================

async def main():
    topics = ["Introduction to Deep Learning"]
    print("\n" + "🎓 SAVITRI ACADEMIC READER ".center(60, "="))
    for topic in topics:
        await run_savitri_for_topic(topic)
    print("\n" + "✅ SESSION COMPLETE ".center(60, "="))

if __name__ == "__main__":
    asyncio.run(main())
