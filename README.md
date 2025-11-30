# 🎙️ Text to Humanoid Voice Converter  
A next-generation **AI-powered speech generation system** that transforms **any text or file** into natural, human-like speech.  
This project supports multi-language detection, file-to-text extraction, voice cloning, and multiple TTS engines — all wrapped in a clean, production-ready architecture.

---

## ✨ Key Features

### 🧠 **Smart Language Detection**
Automatically detects language using `langdetect` and optimizes text for correct pronunciation.  
Supports: **English (en), Urdu (ur), Arabic (ar), Spanish (es), French (fr)**.

---

## 🔊 **Ultra-Realistic TTS (Humanoid Voice Generation)**  
Multiple TTS engines are integrated:

### 🎤 **1. Coqui XTTS-v2 (Human-like Voice + Speaker Reference)**
- Uses **speaker_wav** to mimic a human voice  
- High quality multilingual TTS  
- GPU supported  
- Splits long paragraphs into chunks for smooth output  

### 🌐 **2. Google gTTS (Fast & Lightweight)**  
- Great fallback engine  
- Very fast  
- Supports many languages  

### 💻 **3. pyttsx3 (Offline Local Engine)**  
- Works without internet  
- Uses system voices  
- Stable for long text  

### 🔊 **4. ElevenLabs API (Premium TTS)**  
- Ultra-natural commercial-grade voices  

---

## 📂 **File-to-Audio Conversion (Auto Extraction)**  
This system can convert **ANY supported file into speech**:

| File Type | Extraction Method |
|----------|-------------------|
| PDF | pdfplumber |
| DOCX | python-docx |
| Image (PNG/JPG) | Tesseract OCR |
| TXT | UTF-8 reader |

📌 **Just upload a file → AI extracts text → Generates humanoid audio.**

---

## 🛠️ **Text Cleaning & Preprocessing**
Includes a full preprocessing pipeline:
- Removes noise, invalid characters, emojis  
- Normalizes spacing  
- Fixes punctuation  
- Splits long text into optimized chunks  
- Converts abbreviations (Dr. → Doctor, Mr. → Mister)  
- Removes URLs, emails, unwanted symbols  

This ensures **high-quality, natural TTS output**.

---

## 📦 Project Modules

📁 Module 1: File Text Extraction
→ PDF | DOCX | Images (OCR) | TXT

📁 Module 2: Language Detection & Preprocessing
→ detect_language()
→ preprocess_text()
→ split_text_into_chunks()

📁 Module 3: Humanoid Speech Generation (TTS)
→ Coqui XTTS-v2 (voice cloning)
→ gTTS
→ pyttsx3
→ ElevenLabs

📁 Module 4: Audio Post-Processing
→ Merging chunks
→ WAV → MP3 conversion

