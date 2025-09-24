from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

import pandas as pd
import io
import json

def get_llm(api_key: str):
    """Retorna uma instância do LLM Gemini Flash."""
    return ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", google_api_key=api_key, temperature=0.1)

def get_dataset_preview(df: pd.DataFrame) -> str:
    """Gera uma prévia textual do dataframe para o prompt."""
    buffer = io.StringIO()
    df.info(buf=buffer)
    info_str = buffer.getvalue()

    preview = f"""
    ### Informações do Dataset
    - Shape (Linhas, Colunas): {df.shape}
    - Primeiras 5 linhas:
    {df.head().to_string()}
    - Tipos de Dados e Valores Não-Nulos:
    {info_str}
    - Estatísticas Descritivas (Numéricas):
    {df.describe().to_string()}
    """
    return preview