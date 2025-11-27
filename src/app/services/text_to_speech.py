from sarvamai import SarvamAI
from app.config import SARVAM_API_KEY
import base64

client = SarvamAI(api_subscription_key=SARVAM_API_KEY)

async def synthesize_audio(text: str, target_language_code: str) -> bytes:
    """
    Converts text to speech using Sarvam AI (Bulbul).
    Returns audio bytes (WAV/MP3).
    """
    try:
        # Sarvam TTS API
        # Based on docs: client.text_to_speech.create(...)
        # Need to map language code to speaker if required, or let API handle it.
        # Bulbul supports various languages.
        
        response = client.text_to_speech.convert(
            text=text,
            target_language_code=target_language_code,
            model="bulbul:v2" 
        )
        
        # Response likely contains audio bytes or base64.
        # If it returns base64 string, decode it.
        # If it returns bytes, return as is.
        
        # Assuming response has 'audios' list with base64 strings (common pattern)
        # or 'audio' field.
        # Let's assume it returns an object with 'audios' which is a list of base64 strings.
        
        if hasattr(response, 'audios') and response.audios:
            return base64.b64decode(response.audios[0])
        elif isinstance(response, dict) and 'audios' in response:
            return base64.b64decode(response['audios'][0])
        else:
            # Check if it's raw bytes (unlikely for JSON API but possible if SDK handles it)
            # Or maybe 'audio_content'
            print(f"Unexpected TTS response format: {response}")
            raise ValueError("Could not extract audio from TTS response")

    except Exception as e:
        print(f"Error in synthesize_audio: {e}")
        raise e
