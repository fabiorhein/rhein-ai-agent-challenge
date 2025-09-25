# Exemplo de código que será executado automaticamente
# Este código demonstra a execução automática na interface

import pandas as pd
import plotly.express as px

# Usar o DataFrame carregado (df já está disponível)
print("DataFrame shape:", df.shape)
print("Colunas disponíveis:", list(df.columns))

# Criar uma visualização simples
fig = px.scatter(df,
                 x=df.columns[0],  # Primeira coluna como X
                 y=df.columns[1] if len(df.columns) > 1 else df.columns[0],  # Segunda coluna como Y
                 title='Gráfico de Dispersão Automático',
                 color=df.columns[0] if df.dtypes[0] in ['object', 'category'] else None)

# Configurar layout
fig.update_layout(
    showlegend=True,
    font=dict(size=12)
)

# Calcular estatísticas básicas
print("\nEstatísticas descritivas:")
print(df.describe())

# Retornar a figura para ser capturada
result = fig
