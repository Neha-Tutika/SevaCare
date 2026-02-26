# SevaCare
💊 Prescription Reader & Voice Assistant
A FastAPI-powered backend service that extracts structured data from prescription images/PDFs using Google Gemini AI, and reads them aloud in multiple Indian and international languages using Microsoft Edge TTS.

✨ Features

📄 Prescription Upload — Accepts image (PNG, JPG, JPEG) or PDF prescriptions
🤖 AI Extraction — Uses Google Gemini Vision to extract doctor info and medication schedule
🌐 Multi-language Translation — Translates the prescription summary into your preferred language
🔊 Text-to-Speech — Reads out the prescription in natural-sounding voices via Edge TTS
🌍 Supports 10+ Languages — Hindi, Telugu, Tamil, Kannada, Malayalam, Marathi, Bengali, Gujarati, Spanish, French, English


## 🗂️ Project Structure

| File | Description |
|------|-------------|
| `main.py` | FastAPI app with `/upload-prescription` and `/speak` endpoints |
| `prescription_service.py` | Gemini AI extraction + data normalization logic |
| `list_voices.py` | Utility to list Edge TTS voices for Indian locales |
| `client.html` | Frontend HTML client for testing the API |
| `requirements.txt` | Python dependencies |
| `.env.example` | Environment variable template |

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/prescription-reader.git
cd prescription-reader
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

> Get your Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

### 4. Run the Server
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## 📡 API Endpoints

### `POST /upload-prescription`

Uploads a prescription file and extracts structured data using Gemini AI.

| Field | Type | Description |
|-------|------|-------------|
| `file` | File | Image (PNG/JPG) or PDF prescription |
| `language` | String | Target language for translation (default: `Hindi`) |

**Response:**
```json
{
  "status": "success",
  "data": {
    "doctor_name": "Dr. John Smith",
    "doctor_id_external": "MCI12345",
    "drugs": [
      { "drug_name": "Paracetamol 500mg", "slots": ["morning", "night"] }
    ],
    "simple_explanation": "Take Paracetamol twice a day...",
    "translated_explanation": "सुबह और रात को पैरासिटामोल लें..."
  }
}
```

---

### `POST /speak`

Converts text to speech in the specified language using Edge TTS.

| Field | Type | Description |
|-------|------|-------------|
| `text` | String | Text to be spoken |
| `language` | String | Language name or code (e.g., `Hindi`, `hi`, `hi-IN`) |

**Response:** Audio stream (`audio/mpeg`)

---

### `GET /`

Health check — returns a confirmation message that the service is running.

🧪 Testing
Open client.html in your browser to use the built-in frontend for uploading prescriptions and playing back audio.
Alternatively, use the interactive API docs at:
http://localhost:8000/docs

📦 Dependencies

FastAPI — Web framework
Google Generative AI — Gemini Vision for prescription extraction
Edge TTS — Microsoft Edge Text-to-Speech
Pillow — Image processing
pypdf — PDF text extraction
python-dotenv — Environment variable management


⚠️ Important Notes

File size limit: 5MB per upload
Supported formats: PNG, JPG, JPEG, PDF
If Gemini API key is not set, the service runs in mock mode and returns dummy data for testing
PDF files must contain selectable text; scanned PDFs should be submitted as images instead
