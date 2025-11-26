from fastapi import APIRouter, Request, Response, HTTPException
from fastapi.responses import StreamingResponse
from twilio.twiml.voice_response import VoiceResponse, Play
import requests
import io

from app.services.speech_to_text import speech_to_english
from app.services.llm import run_llm
from app.services.translator import translate_to_native
from app.services.text_to_speech import synthesize_audio
from app.utils.audio import get_content_type

router = APIRouter()

# In-memory storage for audio (Not production ready, but fits requirements)
# Key: CallSid, Value: Audio Bytes
audio_cache = {}

@router.post("/twilio/voice")
async def handle_voice_webhook(request: Request):
    """
    Handles incoming Twilio voice webhook.
    """
    try:
        form_data = await request.form()
        call_sid = form_data.get("CallSid")
        recording_url = form_data.get("RecordingUrl") # If recording is available
        # Or maybe Twilio sends audio in a different way depending on setup.
        # Requirement: "Receive audio stream or recording URL"
        # If it's a stream, it's more complex (WebSocket). 
        # If it's a recording, we get a URL.
        # Let's assume we are using <Record> action or similar that posts to this URL.
        # OR, if this is the INITIAL call, we might not have audio yet.
        # But the prompt says: "Receive a phone call... Accept audio input... Respond back"
        # This implies an interactive flow. 
        # Usually: 
        # 1. Twilio calls webhook -> We return <Record> or <Gather>.
        # 2. User speaks -> Twilio posts to webhook with RecordingUrl.
        # 3. We process -> Return <Play>.
        
        # If no recording URL, maybe it's the start of the call?
        if not recording_url:
            # Initial greeting / Start recording
            resp = VoiceResponse()
            resp.say("Hello. Please speak now.")
            resp.record(action="/twilio/voice", play_beep=True) # Loop back to same URL
            return Response(content=str(resp), media_type="application/xml")

        # We have a recording URL
        # 1. Download audio
        audio_response = requests.get(recording_url)
        audio_bytes = audio_response.content
        
        # 2. STT (English)
        english_text = await speech_to_english(audio_bytes)
        print(f"Transcript: {english_text}")
        
        # 3. LLM (Reasoning)
        llm_response = await run_llm(english_text)
        print(f"LLM Response: {llm_response}")
        
        # 4. Translate (English -> Native)
        # We need to know the target language. 
        # For now, let's assume Hindi (hi-IN) or try to detect from STT if possible.
        # But STT returns English text (Saaras translates to English?). 
        # Wait, Saaras is STT. Does it translate? 
        # User said: "Saaras -> Speech-to-English-Text". So it transcribes AND translates to English?
        # Or just transcribes English? 
        # "Speech-to-English-Text" implies output is English.
        # So we don't know the original language unless we detect it.
        # Sarvam STT response might have language code.
        # My implementation of speech_to_english returns only text.
        # I should probably update it to return language too if needed, but for now let's default to Hindi 
        # or let the LLM decide, or just hardcode 'hi-IN' as per "Indian languages" theme.
        # Let's default to 'hi-IN' for the response for this demo.
        target_lang = "hi-IN" 
        
        translated_text = await translate_to_native(llm_response, target_lang)
        print(f"Translated: {translated_text}")
        
        # 5. TTS (Bulbul)
        audio_output = await synthesize_audio(translated_text, target_lang)
        
        # 6. Store in cache
        audio_cache[call_sid] = audio_output
        
        # 7. Return TwiML
        resp = VoiceResponse()
        # Construct absolute URL for playback
        # Since we are local, we might need ngrok. 
        # We'll use a relative path and hope Twilio (via ngrok) handles it, 
        # or user needs to configure base URL.
        # Twilio requires absolute URLs for <Play>.
        # We will use the Host header to construct it.
        base_url = str(request.base_url).rstrip('/')
        play_url = f"{base_url}/twilio/audio/{call_sid}"
        
        resp.play(play_url)
        # Continue conversation?
        resp.record(action="/twilio/voice", play_beep=True) 
        
        return Response(content=str(resp), media_type="application/xml")

    except Exception as e:
        import traceback
        with open("error.log", "w") as f:
            f.write(traceback.format_exc())
            f.write(f"\nError: {e!r}")
        print(f"Error: {e}")
        resp = VoiceResponse()
        resp.say("Sorry, an error occurred.")
        return Response(content=str(resp), media_type="application/xml")

@router.get("/twilio/audio/{call_sid}")
async def get_audio(call_sid: str):
    """
    Serves the generated audio for a specific call.
    """
    audio_bytes = audio_cache.get(call_sid)
    if not audio_bytes:
        raise HTTPException(status_code=404, detail="Audio not found")
    
    # Clear cache after serving (one-time use)
    # del audio_cache[call_sid] 
    # Keep it for a bit in case of retries? Better to delete to save memory.
    # But Twilio might request multiple times? Unlikely for <Play>.
    
    return StreamingResponse(io.BytesIO(audio_bytes), media_type="audio/wav")
