# SevaCare
SevaCare allows users to upload prescription images or PDFs and automatically extracts structured medical information using AI. The system identifies the doctor’s name, registration ID (if available), prescribed medications, and intake timings such as morning, afternoon, or night.
Beyond basic extraction, SevaCare generates a simple and easy-to-understand explanation in English, making medical instructions clearer for patients. It also provides automatic translation into a selected regional language to improve accessibility for non-English speakers.
The platform includes file validation for supported formats and size limits, structured JSON output for easy database storage, medication slot normalization, and strong error handling for API limits or invalid uploads. The architecture is designed to easily integrate with reminder systems and digital health platforms in the future.

Tech Stack
SevaCare is built using Python as the core programming language, with FastAPI powering the backend API for handling uploads and AI processing. For AI-based prescription extraction and understanding, the project uses the Google Gemini Vision API.
Image processing is handled using Pillow (PIL), while pypdf is used to extract text from uploaded PDF prescriptions. Environment variables and API key management are handled through python-dotenv, and structured outputs are managed using JSON parsing and validation logic.
The system can be connected to a frontend built with Streamlit or a web-based client interface, making it flexible for demonstration and deployment.
