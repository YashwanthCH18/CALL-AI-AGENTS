from sarvamai import SarvamAI
from app.config import SARVAM_API_KEY
import io

# Initialize Sarvam Client
client = SarvamAI(api_subscription_key=SARVAM_API_KEY)

async def speech_to_english(audio_bytes: bytes) -> tuple[str, str]:
    """
    Transcribes audio bytes to English text using Sarvam AI (Saarika/Saaras).
    Returns a tuple of (transcript, detected_language_code).
    """
    try:
        # Create a file-like object from bytes
        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = "audio.wav" 

        response = client.speech_to_text.transcribe(
            file=audio_file,
            model="saarika:v2.5", 
        )
        
        # Extract transcript and language_code
        # Response object should have 'transcript' and 'language_code'
        transcript = ""
        language_code = "hi-IN" # Default fallback

        if hasattr(response, 'transcript'):
            transcript = response.transcript
        elif isinstance(response, dict) and 'transcript' in response:
            transcript = response['transcript']
            
        if hasattr(response, 'language_code'):
            language_code = response.language_code
        elif isinstance(response, dict) and 'language_code' in response:
            language_code = response['language_code']
            
        return transcript, language_code

    except Exception as e:
        print(f"Error in speech_to_english: {e}")
        raise e
