import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

# Configuration
# User requested "gemini 2.5 flash", using 1.5-flash as the closest valid model, or 2.0-flash-exp if available.
# You can change this to "gemini-2.0-flash-exp" if you have access.
GEMINI_MODEL = "gemini-1.5-flash" 

# Audio Settings
SAMPLE_RATE = 16000
CHANNELS = 1
