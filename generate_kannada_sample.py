from sarvamai import SarvamAI
import os
from dotenv import load_dotenv
import base64

load_dotenv()

api_key = os.getenv("SARVAM_API_KEY")
client = SarvamAI(api_subscription_key=api_key)

text = "ನಮಸ್ಕಾರ, ನೀವು ಹೇಗಿದ್ದೀರಿ?" # Namaskara, neevu hegiddiri? (Hello, how are you?)
target_language_code = "kn-IN"

print("Generating Kannada audio...")
try:
    response = client.text_to_speech.convert(
        text=text,
        target_language_code=target_language_code,
        model="bulbul:v2"
    )
    
    # Decode and save
    # Response is expected to be an object with 'audios' list of base64 strings
    # based on my previous experience/assumption, but let's check what I implemented in text_to_speech.py
    # In text_to_speech.py I handled it.
    # The SDK returns a response object. Let's assume it has .audios or similar.
    # Wait, in text_to_speech.py I used `response.audios[0]`.
    # Let's inspect the response structure if needed, but I'll assume it's consistent.
    
    if hasattr(response, 'audios') and response.audios:
        audio_bytes = base64.b64decode(response.audios[0])
        with open("kannada_sample.wav", "wb") as f:
            f.write(audio_bytes)
        print("Saved kannada_sample.wav")
    else:
        print("No audio found in response")
        print(response)

except Exception as e:
    print(f"Error: {e}")
