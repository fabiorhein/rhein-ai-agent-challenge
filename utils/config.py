import os
from dotenv import load_dotenv

load_dotenv()

def get_config():
    """Carrega e retorna as configurações de variáveis de ambiente."""
    return {
        "google_api_key": os.getenv("GOOGLE_API_KEY"),
        "supabase_url": os.getenv("SUPABASE_URL"),
        "supabase_key": os.getenv("SUPABASE_KEY"),
    }