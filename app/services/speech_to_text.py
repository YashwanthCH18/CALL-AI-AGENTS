from sarvamai import SarvamAI
from app.config import SARVAM_API_KEY
import io

# Initialize Sarvam Client
client = SarvamAI(api_subscription_key=SARVAM_API_KEY)

async def speech_to_english(audio_bytes: bytes) -> str:
    """
    Transcribes audio bytes to English text using Sarvam AI (Saarika/Saaras).
    Defaults to 'saarika:v2.5' as per documentation.
    """
    try:
        # Create a file-like object from bytes
        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = "audio.wav" # Sarvam SDK might check extension

        # Call Sarvam STT API
        # Using synchronous call as the SDK seems synchronous based on docs, 
        # but wrapping in async function for FastAPI.
        # If SDK supports async, we should await it. 
        # Based on quickstart: response = client.speech_to_text.transcribe(...)
        
        response = client.speech_to_text.transcribe(
            file=audio_file,
            model="saarika:v2.5", # Using saarika:v2.5 as default STT model
            # language_code="unknown" # Let it detect or specify if known
        )
        
        # Extract transcript
        # Response structure: {'transcript': '...', ...} or object
        # Assuming response is an object or dict. 
        # Quickstart print(response) suggests it returns a response object.
        # I'll assume it has a transcript attribute or key.
        
        if hasattr(response, 'transcript'):
            return response.transcript
        elif isinstance(response, dict) and 'transcript' in response:
            return response['transcript']
        else:
            # Fallback/Debug
            return str(response)

    except Exception as e:
        print(f"Error in speech_to_english: {e}")
        raise e
