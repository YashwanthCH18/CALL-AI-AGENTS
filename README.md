# Voice AI Microservice

This is a FastAPI microservice that handles AI voice calling in Indian languages using Twilio, Sarvam AI, and Gemini.

## Features
- **Speech-to-Text**: Converts user audio to English text using Sarvam AI (Saaras/Saarika). Note: Synchronous API supports up to 30s of audio.
- **Reasoning**: Uses Gemini (Flash) to process the text and generate a response.
- **Translation**: Translates the response to an Indian language (default: Hindi) using Sarvam Translate.
- **Text-to-Speech**: Converts the translated text to speech using Sarvam AI (Bulbul).
- **Twilio Integration**: Handles voice webhooks and plays back the generated audio.

## Prerequisites
- Python 3.8+
- Twilio Account
- Sarvam AI API Key
- Gemini API Key

## Setup

1. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   Create a `.env` file in the `app` directory (or root) with the following keys:
   ```env
   SARVAM_API_KEY=your_sarvam_key
   GEMINI_API_KEY=your_gemini_key
   TWILIO_ACCOUNT_SID=your_twilio_sid
   TWILIO_AUTH_TOKEN=your_twilio_token
   ```

## Running the Service

1. **Start the Server**
   ```bash
   uvicorn app.main:app --reload
   ```
   The server will run at `http://localhost:8000`.

2. **Expose to Internet (for Twilio)**
   Use ngrok to expose your local server:
   ```bash
   ngrok http 8000
   ```
   Copy the HTTPS URL (e.g., `https://xyz.ngrok.io`).

3. **Configure Twilio**
   - Go to your Twilio Phone Number settings.
   - Set the "A call comes in" webhook to `https://xyz.ngrok.io/twilio/voice`.
   - Ensure HTTP method is `POST`.

## Testing Locally

You can use the `dummy_call.py` script to simulate a Twilio webhook call without making a real phone call.

```bash
python dummy_call.py
```

This script will:
1. Send a POST request to `/twilio/voice` with a sample audio URL.
2. Receive the TwiML response.
3. Extract the audio URL from the `<Play>` tag.
4. Download and save the generated audio to `response_audio.wav`.

## Project Structure
```
voice-ai-service/
│── app/
│     ├── main.py              # FastAPI entry point
│     ├── routers/
│     │      └── voice.py      # Twilio webhook handler
│     ├── services/
│     │      ├── speech_to_text.py
│     │      ├── translator.py
│     │      ├── llm.py
│     │      └── text_to_speech.py
│     ├── utils/
│     │      ├── audio.py
│     │      └── helpers.py
│     ├── models/
│     └── config.py
│
│── requirements.txt
│── dummy_call.py              # Verification script
│── README.md
```
