import pandas as pd
from agents.agent_setup import get_llm, get_dataset_preview
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

PROMPT_TEMPLATE = """
Você é o "ConsultantAgent", um consultor de dados sênior com 15 anos de experiência. Sua função é traduzir análises estatísticas em insights de negócio acionáveis.

**Contexto do Dataset:**
{dataset_preview}

**Histórico de Análises Realizadas nesta Sessão:**
{all_analyses}

**Pergunta do Usuário:**
"{user_question}"

**Sua Tarefa:**
Com base em todas as informações disponíveis, forneça uma resposta que inclua:
1.  **Insights de Negócio**: O que os números e gráficos significam em um contexto prático? Quais são as implicações?
2.  **Conclusões Baseadas em Evidências**: Sintetize as descobertas mais importantes.
3.  **Recomendações Estratégicas (se aplicável)**: Sugira ações que poderiam ser tomadas com base nos dados.
4.  **Identificação de Oportunidades e Riscos**: Aponte tendências positivas ou negativas, anomalias preocupantes ou potenciais áreas de melhoria.

Mantenha um tom profissional, confiante e focado em gerar valor de negócio. Use Markdown para estruturar sua resposta.
"""

def get_consultant_agent(api_key: str):
    llm = get_llm(api_key)
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    chain = prompt | llm | StrOutputParser()
    return chain

def run_consultant(api_key: str, df: pd.DataFrame, all_analyses: str, user_question: str):
    agent = get_consultant_agent(api_key)
    dataset_preview = get_dataset_preview(df)
    response = agent.invoke({
        "dataset_preview": dataset_preview,
        "all_analyses": all_analyses,
        "user_question": user_question
    })
    return response