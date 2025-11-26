import google.generativeai as genai
from app.config import GEMINI_API_KEY, GEMINI_MODEL

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

async def run_llm(prompt: str) -> str:
    """
    Sends a prompt to Gemini and returns the response text.
    """
    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error in run_llm: {e}")
        # Fallback or re-raise
        return "I'm sorry, I couldn't process that."
