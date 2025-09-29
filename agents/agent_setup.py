from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate
import pandas as pd
import io
import json
import requests

class ModelFallbackError(Exception):
    """Exceção para quando ocorre um erro e precisamos tentar outro modelo"""
    pass

def get_llm(api_key: str, model_type: str = "gemini-flash", **kwargs):
    """
    Retorna uma instância do LLM selecionado com fallback automático.
    
    Args:
        api_key: Chave de API para o serviço
        model_type: Tipo de modelo a ser usado ('gemini-flash' ou 'huggingface')
        **kwargs: Argumentos adicionais específicos do modelo
    """
    temperature = kwargs.get('temperature', 0.0)
    
    try:
        if model_type == "gemini-flash":
            try:
                return ChatGoogleGenerativeAI(
                    model="gemini-2.0-flash",
                    google_api_key=api_key,
                    temperature=temperature,
                    request_timeout=30
                )
            except Exception as e:
                print(f"Erro ao conectar ao Gemini: {e}")
                if model_type == "gemini-flash":  # Se já tentamos o fallback e falhou
                    raise ModelFallbackError("Falha ao conectar ao Gemini")
                raise
                
        elif model_type == "huggingface":
            if not api_key:
                raise ModelFallbackError("Chave de API do Hugging Face ausente")
            try:
                return HuggingFaceEndpoint(
                    repo_id="mistralai/Mistral-7B-Instruct-v0.2",
                    task="text-generation",
                    huggingfacehub_api_token=api_key,
                    temperature=temperature,
                    max_new_tokens=1024
                )
            except Exception as e:
                print(f"Erro ao conectar ao Hugging Face: {e}")
                raise ModelFallbackError("Falha ao conectar ao Hugging Face")
                
        else:
            raise ValueError(f"Modelo não suportado: {model_type}")
            
    except Exception as e:
        print(f"Erro ao criar LLM: {e}")
        raise

def get_llm_with_fallback(api_keys_config, model_choice=None):
    """
    Tenta criar um LLM com fallback automático.
    
    Args:
        api_keys_config: Dicionário com as chaves de API
        model_choice: Modelo escolhido pelo usuário (None para usar o padrão)
    """
    model_choice = model_choice or api_keys_config.get("default_model", "gemini-flash")
    
    try:
        if model_choice == "gemini-flash":
            return get_llm(api_keys_config.get("google_api_key"), "gemini-flash")
        elif model_choice == "huggingface":
            return get_llm(api_keys_config.get("hf_api_key"), "huggingface")
    except ModelFallbackError:
        # Se o modelo escolhido falhar, tenta o outro
        fallback = "huggingface" if model_choice == "gemini-flash" else "gemini-flash"
        print(f"Tentando fallback para: {fallback}")
        try:
            if fallback == "gemini-flash":
                return get_llm(api_keys_config.get("google_api_key"), "gemini-flash")
            else:
                return get_llm(api_keys_config.get("hf_api_key"), "huggingface")
        except Exception as e:
            raise Exception(f"Falha em todos os modelos disponíveis: {e}")

def get_dataset_preview(df: pd.DataFrame) -> str:
    """Preview compacto para reduzir tokens."""
    MAX_COLS = 30
    MAX_ROWS_SAMPLE = 3
    cols = df.columns.tolist()[:MAX_COLS]
    dtypes = {c: str(df.dtypes[c]) for c in cols}
    sample = df[cols].head(MAX_ROWS_SAMPLE).to_dict(orient="records")

    preview = (
        f"Shape: {df.shape}\n"
        f"Columns (limited to {MAX_COLS}): {cols}\n"
        f"Dtypes: {dtypes}\n"
        f"Sample first {MAX_ROWS_SAMPLE} rows (dict): {sample}\n"
    )
    return preview