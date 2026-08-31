import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
    
    # Supabase setup
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    
    # Model preferences
    DEFAULT_LLM = "mistral-large-latest" # Using Mistral's flagship model

settings = Settings()
