import os
import sys

if sys.version_info >= (3, 11):
    import tomllib
else:
    import toml as tomllib

def get_config():
    """Carrega e retorna as configurações do secrets.toml."""
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.streamlit', 'secrets.toml')

    try:
        with open(config_path, 'rb') as f:
            config_data = tomllib.load(f)

        app_config = config_data.get('custom', {})

        return {
            "google_api_key": app_config.get("google_api_key"),
            "hf_api_key": app_config.get("hf_api_key"),  # Nova chave do Hugging Face
            "default_model": app_config.get("default_model", "gemini-flash"),  # Modelo padrão
            "supabase_url": app_config.get("supabase_url"),
            "supabase_key": app_config.get("supabase_key"),
        }
    except FileNotFoundError:
        print("Aviso: Arquivo secrets.toml não encontrado. Usando variáveis de ambiente como fallback.")
        # Fallback para variáveis de ambiente
        return {
            "google_api_key": os.getenv("GOOGLE_API_KEY"),
            "hf_api_key": os.getenv("HF_API_KEY"),  # Nova variável de ambiente
            "default_model": os.getenv("DEFAULT_MODEL", "gemini-flash"),
            "supabase_url": os.getenv("SUPABASE_URL"),
            "supabase_key": os.getenv("SUPABASE_KEY"),
        }
    except Exception as e:
        print(f"Erro ao carregar secrets.toml: {e}")
        return {
            "google_api_key": None,
            "hf_api_key": None,
            "default_model": None,
            "supabase_url": None,
            "supabase_key": None,
        }