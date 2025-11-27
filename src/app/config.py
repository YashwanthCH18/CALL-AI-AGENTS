import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Configuration
# User requested "gemini 2.5 flash"
GEMINI_MODEL = "gemini-2.5-flash" 

# Audio Settings
SAMPLE_RATE = 16000
CHANNELS = 1
