from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from prescription_service import extract_prescription_data, validate_upload_file, normalize_extracted_data

app = FastAPI(title="Prescription Upload Service")

# Enable CORS - allows requests from any website
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload-prescription")
async def upload_prescription(
    file: UploadFile = File(...),
    language: str = Form("Hindi")
):
    # Step 1: Validate the uploaded file
    is_valid, error = await validate_upload_file(file)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error)
    
    # Step 2: Extract data using Gemini AI
    raw_data = await extract_prescription_data(file, language)
    
    # Step 3: Normalize and validate the data
    normalized_data = normalize_extracted_data(raw_data)
    
    return {"status": "success", "data": normalized_data}

import edge_tts
import io
import tempfile
import os
from fastapi.responses import FileResponse, StreamingResponse

@app.post("/speak")
async def speak(text: str = Form(...), language: str = Form("en")):
    """
    Generate TTS audio using Edge TTS (better quality and faster)
    """
    try:
        # Map our display languages to Edge TTS voice IDs
        # Microsoft Edge Voice List: https://github.com/rnotario/edge-tts/blob/master/VOICES.md
        voice_map = {
            "Hindi": "hi-IN-SwaraNeural",
            "Telugu": "te-IN-MohanNeural", 
            "Tamil": "ta-IN-PallaviNeural",
            "Kannada": "kn-IN-GaganNeural",
            "Malayalam": "ml-IN-SobhanaNeural",
            "Marathi": "mr-IN-AarohiNeural",
            "Bengali": "bn-IN-TanishaaNeural",
            "Gujarati": "gu-IN-DhwaniNeural",
            "Spanish": "es-ES-ElviraNeural",
            "French": "fr-FR-DeniseNeural",
            "English": "en-US-AriaNeural"
        }
        
        # Log the request for debugging
        print(f"Generating audio for language: {language}, text length: {len(text)}")

        # Use mapped voice or default to a generic English voice
        voice = voice_map.get(language, "en-US-AriaNeural")
        
        # Enhanced fallback logic:
        # 1. Handle short codes (e.g., 'hi')
        if language == "hi": voice = "hi-IN-SwaraNeural"
        if language == "te": voice = "te-IN-MohanNeural"
        if language == "ta": voice = "ta-IN-PallaviNeural"
        if language == "kn": voice = "kn-IN-GaganNeural"
        if language == "ml": voice = "ml-IN-SobhanaNeural"
        if language == "mr": voice = "mr-IN-AarohiNeural"
        if language == "bn": voice = "bn-IN-TanishaaNeural"
        if language == "gu": voice = "gu-IN-DhwaniNeural"

        # 2. Handle full codes (e.g., 'te-IN') directly if they match the start of a voice ID
        # or use a smarter lookup based on the list we know exists.
        
        # If language contains '-IN' (e.g., 'te-IN'), map it to the corresponding voice
        if language == "hi-IN": voice = "hi-IN-SwaraNeural"
        if language == "te-IN": voice = "te-IN-MohanNeural"
        if language == "ta-IN": voice = "ta-IN-PallaviNeural"
        if language == "kn-IN": voice = "kn-IN-GaganNeural"
        if language == "ml-IN": voice = "ml-IN-SobhanaNeural"
        if language == "mr-IN": voice = "mr-IN-AarohiNeural"
        if language == "bn-IN": voice = "bn-IN-TanishaaNeural"
        if language == "gu-IN": voice = "gu-IN-DhwaniNeural"
        
        print(f"Selected voice: {voice}")

        communicate = edge_tts.Communicate(text, voice)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_filename = fp.name
            
        await communicate.save(temp_filename)
        
        with open(temp_filename, "rb") as f:
            audio_data = f.read()
            
        os.unlink(temp_filename) # Delete temp file
        
        print(f"Audio generated successfully, size: {len(audio_data)} bytes")
        return StreamingResponse(io.BytesIO(audio_data), media_type="audio/mpeg")

    except Exception as e:
        print(f"Edge TTS Error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"message": "Prescription Upload Service is running!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)