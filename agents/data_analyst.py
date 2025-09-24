import pandas as pd
from agents.agent_setup import get_llm, get_dataset_preview
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

PROMPT_TEMPLATE = """
Você é o "DataAnalystAgent", um especialista em análise de dados com PhD em Estatística. Sua tarefa é analisar o dataset fornecido e responder à pergunta do usuário de forma precisa e técnica.

**Contexto da Análise:**
{dataset_preview}

**Histórico da Conversa e Análises Anteriores:**
{analysis_context}

**Pergunta Específica para Você:**
"{specific_question}"

**Sua Resposta Deve Conter:**
1.  **Análise Direta**: Responda à pergunta com análises estatísticas detalhadas.
2.  **Métricas Relevantes**: Forneça números específicos (médias, medianas, desvios padrão, correlações, p-values, etc.).
3.  **Observações Técnicas**: Aponte padrões estatisticamente significativos, outliers (usando IQR ou Z-score), ou qualquer outra descoberta relevante.
4.  **Concisão**: Seja objetivo e foque nos dados. Não forneça conclusões de negócio, apenas os fatos analíticos.

Formate sua resposta usando Markdown para clareza.
"""

def get_data_analyst_agent(api_key: str):
    llm = get_llm(api_key)
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    chain = prompt | llm | StrOutputParser()
    return chain

def run_data_analyst(api_key: str, df: pd.DataFrame, analysis_context: str, specific_question: str):
    agent = get_data_analyst_agent(api_key)
    dataset_preview = get_dataset_preview(df)
    response = agent.invoke({
        "dataset_preview": dataset_preview,
        "analysis_context": analysis_context,
        "specific_question": specific_question
    })
    return response