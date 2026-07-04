# 🛍️ Smart Shopping Assistant

An AI-powered shopping assistant that uses **Computer Vision (OCR)** to detect product names from screenshots, then provides instant verdicts, pros & cons, reviews, alternatives, and a chat interface.

## Features
- 📷 Upload a product screenshot — OCR detects the product name automatically
- ✅ AI verdict: Buy / Avoid / Wait for Sale badge
- ⭐ Rating out of 10 with pros & cons breakdown
- 📝 Real-time review search and summarization
- 🔄 Alternative product suggestions
- 💬 Chat with AI about the product
- ⚖️ Compare two products side by side
- 📋 Analysis history saved locally

## Tech Stack
- **Computer Vision:** Tesseract OCR + bounding box geometry
- **AI:** Groq API (Llama 3.3)
- **Search:** DuckDuckGo Search (ddgs)
- **UI:** Streamlit
- **Language:** Python

## Setup

### 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/SmartProductAgent.git
cd SmartProductAgent

### 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Install Tesseract OCR
Download and install from: https://github.com/UB-Mannheim/tesseract/wiki
Default path: C:\Program Files\Tesseract-OCR\tesseract.exe

### 5. Set up API keys
Create a `.env` file in the root folder:
GROQ_API_KEY=your_groq_api_key_here

### 6. Run the app
streamlit run app.py

## Project Structure
- `app.py` — Main Streamlit application
- `ocr/` — Tesseract OCR text extraction with bounding box analysis
- `agent/` — AI agents for verdict, search, chat, comparison, history