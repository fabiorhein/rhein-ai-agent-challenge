# Exemplo de código que funciona com o DataFrame já carregado
# Este código usa o 'df' que já está disponível no ambiente

import pandas as pd
import plotly.express as px

# O DataFrame 'df' já está carregado e disponível
# Não é necessário fazer df = pd.read_csv('arquivo.csv')

print("DataFrame shape:", df.shape)
print("Colunas disponíveis:", list(df.columns))

# Criar uma visualização usando o DataFrame carregado
# Selecionar colunas numéricas para análise
numeric_cols = df.select_dtypes(include=['number']).columns

if len(numeric_cols) >= 2:
    # Criar scatter plot entre as duas primeiras colunas numéricas
    fig = px.scatter(df,
                     x=numeric_cols[0],
                     y=numeric_cols[1],
                     title=f'Relação entre {numeric_cols[0]} e {numeric_cols[1]}',
                     labels={
                         numeric_cols[0]: numeric_cols[0].replace('_', ' ').title(),
                         numeric_cols[1]: numeric_cols[1].replace('_', ' ').title()
                     })

    # Configurar layout
    fig.update_layout(
        showlegend=True,
        font=dict(size=12)
    )

    print(f"Gráfico criado entre {numeric_cols[0]} e {numeric_cols[1]}")

elif len(numeric_cols) == 1:
    # Se só há uma coluna numérica, criar histograma
    fig = px.histogram(df,
                       x=numeric_cols[0],
                       title=f'Distribuição de {numeric_cols[0]}',
                       labels={numeric_cols[0]: numeric_cols[0].replace('_', ' ').title()})

    print(f"Histograma criado para {numeric_cols[0]}")

else:
    # Se não há colunas numéricas, mostrar erro
    print("Erro: Não foram encontradas colunas numéricas no DataFrame")
    fig = None

# Calcular estatísticas básicas
print("\nEstatísticas descritivas:")
print(df.describe())

# Retornar a figura para ser capturada pelo sistema
if fig is not None:
    result = fig
    print("✅ Visualização criada com sucesso!")
else:
    print("❌ Não foi possível criar visualização")
