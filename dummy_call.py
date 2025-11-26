import requests
import time
import xml.etree.ElementTree as ET

# Configuration
BASE_URL = "http://localhost:8000"
WEBHOOK_URL = f"{BASE_URL}/twilio/voice"
# Sample audio file (Kannada speech)
SAMPLE_AUDIO_URL = "http://localhost:8001/kannada_sample.wav" 

def simulate_call():
    print("--- Simulating Twilio Call ---")
    
    # 1. Simulate Twilio Webhook (POST)
    payload = {
        "CallSid": "CA1234567890abcdef",
        "RecordingUrl": SAMPLE_AUDIO_URL
    }
    
    print(f"Sending POST request to {WEBHOOK_URL}...")
    try:
        response = requests.post(WEBHOOK_URL, data=payload)
        response.raise_for_status()
        print("Response received!")
        print(f"Status Code: {response.status_code}")
        print(f"Content Type: {response.headers.get('content-type')}")
        print("Response Body (TwiML):")
        print(response.text)
        
        # 2. Parse TwiML to find <Play> URL
        root = ET.fromstring(response.text)
        play_element = root.find("Play")
        if play_element is not None:
            play_url = play_element.text
            print(f"\nFound <Play> URL: {play_url}")
            
            # 3. Fetch the generated audio
            # Note: The URL in TwiML might be absolute or relative depending on implementation
            # In my implementation, I constructed an absolute URL based on request.base_url
            
            print(f"Fetching generated audio from {play_url}...")
            audio_response = requests.get(play_url, stream=True)
            audio_response.raise_for_status()
            
            # Save to file
            output_filename = "response_audio.wav"
            with open(output_filename, "wb") as f:
                for chunk in audio_response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"Audio saved to {output_filename}")
            print("Verification Successful!")
            
        else:
            print("Error: <Play> element not found in TwiML.")
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    simulate_call()
