import google.generativeai as genai
from app.config import GEMINI_API_KEY, GEMINI_MODEL

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

async def run_llm(prompt: str, history: list = None) -> str:
    """
    Sends a prompt to Gemini and returns the response text.
    Supports conversation history.
    """
    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        
        if history:
            # Convert history to Gemini format
            # History format: [{"role": "user", "parts": ["..."]}, {"role": "model", "parts": ["..."]}]
            chat = model.start_chat(history=history)
            response = chat.send_message(prompt)
        else:
            response = model.generate_content(prompt)
            
        return response.text
    except Exception as e:
        print(f"Error in run_llm: {e}")
        # Fallback or re-raise
        return "I'm sorry, I couldn't process that."
