import requests
import time
import xml.etree.ElementTree as ET

# Configuration
BASE_URL = "http://localhost:8000"
WEBHOOK_URL = f"{BASE_URL}/twilio/voice"
# Sample audio file (Kannada speech)
SAMPLE_AUDIO_URL = "http://localhost:8001/kannada_sample.wav" 
CALL_SID = "CA_TEST_123"
PIN = "1234" # Matches the dummy user in Supabase

def simulate_call():
    print("--- Simulating Twilio Call Flow ---")
    
    # 1. Initial Call (Start)
    print("\n[1] Initial Call...")
    payload = {"CallSid": CALL_SID}
    response = requests.post(WEBHOOK_URL, data=payload)
    print(f"Response: {response.text}")
    if "<Gather" in response.text:
        print(">> Success: Asked for PIN")
    else:
        print(">> Failed: Did not ask for PIN")
        # return # Don't return, let's see what happens next for debugging

    # 2. Enter PIN
    print(f"\n[2] Entering PIN: {PIN}...")
    payload = {"CallSid": CALL_SID, "Digits": PIN}
    response = requests.post(WEBHOOK_URL, data=payload)
    print(f"Response: {response.text}")
    if "Hello Yashwanth" in response.text:
        print(">> Success: Authenticated and Greeted")
    else:
        print(">> Failed: Authentication failed")
        return

    # 3. Speak (Send Audio)
    print("\n[3] Speaking (Sending Audio)...")
    payload = {"CallSid": CALL_SID, "RecordingUrl": SAMPLE_AUDIO_URL}
    response = requests.post(WEBHOOK_URL, data=payload)
    
    # Check for Play tag
    if "<Play>" in response.text:
        root = ET.fromstring(response.text)
        play_element = root.find("Play")
        play_url = play_element.text
        print(f">> Success: Response Audio Generated at {play_url}")
        
        # Fetch audio
        audio_response = requests.get(play_url)
        with open("response_auth.wav", "wb") as f:
            f.write(audio_response.content)
        print(">> Audio saved to response_auth.wav")
    else:
        print(">> Failed: No audio response")
        print(response.text)

if __name__ == "__main__":
    simulate_call()
