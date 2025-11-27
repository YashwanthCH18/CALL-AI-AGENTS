from sarvamai import SarvamAI
from app.config import SARVAM_API_KEY

client = SarvamAI(api_subscription_key=SARVAM_API_KEY)

async def translate_to_native(text: str, target_language: str) -> str:
    """
    Translates text from English (or auto) to the target language.
    """
    try:
        # Sarvam Translate API
        # Based on quickstart: response = client.text.translate(...)
        response = client.text.translate(
            input=text,
            source_language_code="en-IN", # Assuming reasoning is in English
            target_language_code=target_language,
            speaker_gender="Female" # Optional, but good for context if TTS follows
        )
        
        # Extract translated text
        if hasattr(response, 'translated_text'):
            return response.translated_text
        elif isinstance(response, dict) and 'translated_text' in response:
            return response['translated_text']
        else:
            return str(response)

    except Exception as e:
        print(f"Error in translate_to_native: {e}")
        return text # Fallback to original text
