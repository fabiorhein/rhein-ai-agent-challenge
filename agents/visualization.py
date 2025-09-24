import pandas as pd
from agents.agent_setup import get_llm, get_dataset_preview
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

PROMPT_TEMPLATE = """
Você é o "VisualizationAgent", um especialista em visualização de dados. Sua tarefa é gerar o código Python para criar um gráfico interativo usando a biblioteca Plotly.

**Contexto da Análise:**
{dataset_preview}

**Análise de Dados Recebida (se houver):**
{analysis_results}

**Pedido do Usuário:**
"{user_request}"

**Sua Tarefa:**
Gere um script Python completo e executável que cria a visualização solicitada usando `plotly.express` ou `plotly.graph_objects`.
O script deve:
1.  Incluir todos os imports necessários (`pandas`, `plotly.express`, etc.).
2.  Conter um placeholder para o carregamento do dataframe, como `df = pd.read_csv('seu_dataset.csv')`. **Não inclua os dados do dataset no código.**
3.  O código do gráfico deve ser claro e seguir as melhores práticas. Use títulos, labels e cores apropriadas.
4.  Terminar com `fig.show()` para exibir o gráfico.

**IMPORTANTE:** Retorne APENAS o bloco de código Python. Não inclua nenhuma explicação, texto introdutório, ou comentários como "Aqui está o código:". A saída deve ser diretamente executável.

**Exemplo de Pedido:** "Crie um histograma da coluna 'idade'."
**Exemplo de Saída Esperada:**
```python
import pandas as pd
import plotly.express as px

# Supondo que o dataframe 'df' já está carregado
# Ex: df = pd.read_csv('seu_dataset.csv')

fig = px.histogram(df, x='idade', title='Distribuição da Idade')
fig.show()"""

def get_visualization_agent(api_key: str):
    llm = get_llm(api_key)
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    chain = prompt | llm | StrOutputParser()
    return chain

def run_visualization(api_key: str, df: pd.DataFrame, analysis_results: str, user_request: str):
    agent = get_visualization_agent(api_key)
    dataset_preview = get_dataset_preview(df)
    # Limpa a saída para garantir que é apenas código
    raw_code = agent.invoke({
        "dataset_preview": dataset_preview,
        "analysis_results": analysis_results,
        "user_request": user_request
    })

    if "```python" in raw_code:
        clean_code = raw_code.split("```python")[1].split("```")[0].strip()
    else:
        clean_code = raw_code.strip()

    return clean_code