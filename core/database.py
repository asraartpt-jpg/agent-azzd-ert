from supabase import create_client, Client
from core.config import settings

def get_supabase_client() -> Client:
    """
    Initializes and returns the Supabase client.
    Ensure SUPABASE_URL and SUPABASE_KEY are set in the environment.
    """
    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        raise ValueError("Supabase credentials are not configured in environment variables.")
    
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

def save_research_session(session_id: str, state_data: dict):
    """
    Saves or updates a research session in the Supabase 'research_sessions' table.
    """
    try:
        supabase = get_supabase_client()
        response = supabase.table("research_sessions").upsert({
            "session_id": session_id,
            "state_data": state_data
        }).execute()
        return response
    except Exception as e:
        print(f"Database Error: {e}")
        return None

def get_research_session(session_id: str):
    """
    Retrieves a research session from Supabase.
    """
    try:
        supabase = get_supabase_client()
        response = supabase.table("research_sessions").select("*").eq("session_id", session_id).execute()
        if response.data:
            return response.data[0].get("state_data")
        return None
    except Exception as e:
        print(f"Database Error: {e}")
        return None
