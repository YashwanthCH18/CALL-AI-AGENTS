from supabase import create_client, Client
from app.config import SUPABASE_URL, SUPABASE_KEY

# Initialize Supabase Client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def verify_user_pin(pin: str) -> dict | None:
    """
    Verifies the user PIN against the 'user_profiles' table.
    Returns user data (dict) if valid, else None.
    """
    try:
        print(f"Verifying PIN: {pin}")
        response = supabase.table("user_profiles").select("*").eq("pin", pin).execute()
        print(f"Supabase Response: {response}")
        
        if response.data and len(response.data) > 0:
            return response.data[0] # Return the first matching user
        else:
            return None
            
    except Exception as e:
        print(f"Error verifying PIN: {e}")
        return None
