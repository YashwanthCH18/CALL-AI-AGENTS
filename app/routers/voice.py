from fastapi import APIRouter, Request, Response, HTTPException
from fastapi.responses import StreamingResponse
from twilio.twiml.voice_response import VoiceResponse, Play, Gather
import requests
import io

from app.services.speech_to_text import speech_to_english
from app.services.llm import run_llm
from app.services.translator import translate_to_native
from app.services.text_to_speech import synthesize_audio
from app.services.auth import verify_user_pin
from app.utils.audio import get_content_type

router = APIRouter()

# In-memory storage for call context
# Key: CallSid
# Value: {
#   "authenticated": bool,
#   "user": dict,
#   "history": list, # Gemini history format
#   "audio_response": bytes # Last generated audio
# }
call_context = {}

@router.post("/twilio/voice")
async def handle_voice_webhook(request: Request):
    """
    Handles incoming Twilio voice webhook.
    """
    try:
        form_data = await request.form()
        call_sid = form_data.get("CallSid")
        digits = form_data.get("Digits") # PIN input
        recording_url = form_data.get("RecordingUrl") # Audio input
        
        # Initialize context if new call
        if call_sid not in call_context:
            call_context[call_sid] = {
                "authenticated": False,
                "user": None,
                "history": [],
                "audio_response": None
            }
            
        context = call_context[call_sid]
        resp = VoiceResponse()

        # --- Step 1: Authentication ---
        if not context["authenticated"]:
            if digits:
                # Verify PIN
                user = await verify_user_pin(digits)
                if user:
                    context["authenticated"] = True
                    context["user"] = user
                    greeting = f"Hello {user['full_name']}. How can I help you today?"
                    resp.say(greeting)
                    resp.record(action="/twilio/voice", play_beep=True, timeout=2, max_length=30)
                else:
                    resp.say("Invalid PIN. Please try again.")
                    gather = Gather(num_digits=4, action="/twilio/voice")
                    gather.say("Please enter your 4 digit PIN.")
                    resp.append(gather)
            else:
                # Ask for PIN
                gather = Gather(num_digits=4, action="/twilio/voice")
                gather.say("Welcome. Please enter your 4 digit PIN.")
                resp.append(gather)
            
            return Response(content=str(resp), media_type="application/xml")

        # --- Step 2: Conversation ---
        
        # If we have a recording, process it
        if recording_url:
            print(f"Downloading audio from: {recording_url}")
            # 1. Download audio
            # Use auth in case "Enforce HTTP Auth" is enabled
            from app.config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
            audio_response = requests.get(recording_url, auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN))
            
            print(f"Audio Download Status: {audio_response.status_code}")
            print(f"Audio Content-Type: {audio_response.headers.get('Content-Type')}")
            
            if audio_response.status_code != 200:
                print(f"Failed to download audio: {audio_response.text}")
                resp.say("Sorry, I could not hear you.")
                return Response(content=str(resp), media_type="application/xml")
                
            audio_bytes = audio_response.content
            
            # 2. STT (English)
            english_text, detected_lang = await speech_to_english(audio_bytes)
            print(f"Transcript: {english_text}, Detected Lang: {detected_lang}")
            
            # Update History (User)
            context["history"].append({"role": "user", "parts": [english_text]})
            
            # 3. LLM (Reasoning) with History
            llm_response = await run_llm(english_text, history=context["history"])
            print(f"LLM Response: {llm_response}")
            
            # Update History (Model)
            context["history"].append({"role": "model", "parts": [llm_response]})
            
            # 4. Translate (English -> Native)
            target_lang = detected_lang
            if not target_lang or target_lang == "unknown":
                 target_lang = "hi-IN" # Fallback
            
            if target_lang != "en-IN":
                translated_text = await translate_to_native(llm_response, target_lang)
            else:
                translated_text = llm_response
                
            print(f"Translated: {translated_text}")
            
            # 5. TTS (Bulbul)
            audio_output = await synthesize_audio(translated_text, target_lang)
            
            # 6. Store in context
            context["audio_response"] = audio_output
            
            # 7. Return TwiML
            base_url = str(request.base_url).rstrip('/')
            play_url = f"{base_url}/twilio/audio/{call_sid}"
            
            resp.play(play_url)
            # Record again with silence detection
            resp.record(action="/twilio/voice", play_beep=False, timeout=2, max_length=30) 
            
            return Response(content=str(resp), media_type="application/xml")
            
        else:
            # Authenticated but no recording (maybe just finished auth greeting)
            # Just wait for input
            # timeout=2 means wait 2 seconds of SILENCE before submitting. 
            # But for initial wait, we might want longer? 
            # No, timeout in <Record> is "End recording after N seconds of silence".
            # We also need to know when to START.
            # <Record> starts immediately.
            resp.record(action="/twilio/voice", play_beep=True, timeout=2, max_length=30)
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
    context = call_context.get(call_sid)
    if not context or not context["audio_response"]:
        raise HTTPException(status_code=404, detail="Audio not found")
    
    return StreamingResponse(io.BytesIO(context["audio_response"]), media_type="audio/wav")
