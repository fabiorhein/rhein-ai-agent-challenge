from agents.agent_setup import get_llm, get_dataset_preview
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

PROMPT_TEMPLATE = """
Você é o "CodeGeneratorAgent", um especialista em gerar código Python limpo e reproduzível para análise de dados.

**Informações do Dataset:**
{dataset_info}

**Análise a ser Convertida em Código:**
{analysis_to_convert}

**Sua Tarefa:**
Gere um script Python que reproduza a análise solicitada. O código deve ser:
- **Completo e Executável**: Inclua todos os imports necessários no topo (`pandas`, `plotly`, etc.).
- **Bem Documentado**: Adicione comentários explicativos.
- **Profissional**: Use boas práticas de programação.
- **Focado**: Retorne APENAS o bloco de código Python, sem nenhum texto ou explicação adicional. A saída deve ser diretamente copiável e executável.

**Exemplo de Análise:** "Cálculo da média da coluna 'price' e plotagem de um histograma."
**Exemplo de Saída Esperada:**
```python
import pandas as pd
import plotly.express as px

# Carregar o dataset (substitua 'seu_dataset.csv' pelo nome do seu arquivo)
# df = pd.read_csv('seu_dataset.csv')

# --- Análise Estatística ---
# Calcula a média da coluna 'price'
# media_price = df['price'].mean()
# print(f"A média de 'price' é: {{media_price}}")

# --- Visualização ---
# Cria um histograma para a distribuição de 'price'
# fig = px.histogram(df, x='price', title='Distribuição de Preços')
# fig.update_layout(bargap=0.1)
# fig.show()
Gere agora o código para a análise fornecida.
"""

def get_code_generator_agent(api_key: str):
    llm = get_llm(api_key)
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    chain = prompt | llm | StrOutputParser()
    return chain

def run_code_generator(api_key: str, dataset_info: str, analysis_to_convert: str):
    agent = get_code_generator_agent(api_key)
    raw_code = agent.invoke({
    "dataset_info": dataset_info,
    "analysis_to_convert": analysis_to_convert
    })
    if "```python" in raw_code:
        clean_code = raw_code.split("```python")[1].split("```")[0].strip()
    else:
        clean_code = raw_code.strip()

    return clean_code
