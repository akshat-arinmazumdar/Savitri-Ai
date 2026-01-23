# Savitri AI 🎧📖

Savitri AI is an advanced, AI-powered academic reader designed to convert textbook PDFs into professional audio lessons. By leveraging neural text-to-speech and large language models, it provides students with a personalized, "human-like" learning experience.

## ✨ Features

- **📄 Smart PDF Processing**: Upload any textbook PDF and let Savitri's AI identify key topics and structures.
- **🎙️ Neural Indian Accent**: Uses the **Neerja (Indian Female)** neural voice for a natural, local academic tone.
- **🧠 AI Summarization**: Automatically generates concise, academic summaries of complex topics using Llama-3.2.
- **🎵 Interactive Dashboard**: A modern React-based UI to manage uploads, view extracted topics, and control playback (Play/Pause).
- **⏳ On-Demand Generation**: Lessons are generated only when you want to hear them, saving processing time and storage.
- **📁 Persistent Playlist**: Once a lesson is generated, it's saved locally for instant replay.

## 🚀 Tech Stack

- **Frontend**: React, Vite, Vanilla CSS (Modern glassmorphic aesthetics).
- **Backend API**: FastAPI (Python).
- **AI Core**: 
  - **Summarization**: Meta-Llama-3.2 (via HuggingFace).
  - **Voice**: Edge-TTS (Neural Neural Engine).
- **Extraction**: `pdfminer.six` / `pdfplumber`.

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/akshat-arinmazumdar/Savitri-Ai.git
cd Savitri-Ai
```

### 2. Backend Setup
```bash
# Activate your virtual environment
venv\Scripts\activate

# The backend requires FastAPI and Uvicorn
pip install fastapi uvicorn edge-tts requests python-multipart
```

### 3. Frontend Setup
```bash
cd venv/react
npm install
```

## 🏃 How to Run

1. **Start the Backend**:
   From the project root:
   ```bash
   python venv/backend/server.py
   ```
   (Running on `http://localhost:8000`)

2. **Start the Frontend**:
   From `venv/react`:
   ```bash
   npm run dev
   ```
   (Access dashboard at `http://localhost:5173`)

## 🌸 Author
Created by Akshat Arin Mazumdar.
---
*Happy Learning with Savitri!*


<img width="1897" height="862" alt="brave_screenshot_localhost" src="https://github.com/user-attachments/assets/357bf168-52cb-46a3-a028-c8509c1b84d8" />




+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++




<img width="1898" height="864" alt="brave_screenshot_localhost (1)" src="https://github.com/user-attachments/assets/f141e0a9-772d-4ad8-82f6-8ef1afd61872" />



