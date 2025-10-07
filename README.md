# InsightAgent EDA - Seu Assistente de Análise de Dados com IA 🤖📊

Uma aplicação inteligente que permite fazer perguntas sobre seus dados em linguagem natural e receber análises completas, gráficos interativos e insights acionáveis.

## 🎨 Melhorias Visuais (Atualizado em Set/2025)

Realizamos melhorias significativas na interface do usuário para melhorar a experiência:

- **Design Moderno e Escuro** - Interface com tema escuro para maior conforto visual
- **Cards de Estatísticas Aprimorados** - Visualização clara e organizada das métricas principais
- **Layout Responsivo** - Adapta-se perfeitamente a diferentes tamanhos de tela
- **Navegação Intuitiva** - Sistema de abas para fácil acesso às diferentes seções de análise
- **Feedback Visual Aprimorado** - Animações sutis e estados de hover para melhor interatividade
- **Tabelas Roláveis** - Visualização otimizada para conjuntos de dados grandes

## 🎯 O que é esta aplicação?

O **InsightAgent EDA** é uma ferramenta de análise exploratória de dados que utiliza inteligência artificial para:

- ✅ **Analisar dados automaticamente** - Faça upload de um arquivo CSV e faça perguntas em português
- ✅ **Gerar gráficos interativos** - Cria visualizações usando Plotly
- ✅ **Fornecer insights de negócio** - Interpreta os dados e dá recomendações práticas
- ✅ **Gerar código Python** - Exporta análises para reutilizar em seus projetos
- ✅ **Preservar histórico** - Mantém suas conversas e análises salvas na nuvem

## 🏗️ Como Funciona?

A aplicação utiliza **5 agentes especializados** que trabalham em conjunto:

### 1. **CoordinatorAgent** 🎯
- **O que faz:** Analisa sua pergunta e decide qual agente é mais adequado
- **Quando usar:** Sempre - é o agente que organiza todo o sistema

### 2. **DataAnalystAgent** 📈
- **O que faz:** Realiza análises estatísticas detalhadas
- **Quando usar:** Para perguntas como:
  - "Qual a média da coluna X?"
  - "Quantos registros temos?"
  - "Existe correlação entre as colunas A e B?"
  - "Quais são os valores únicos?"

### 3. **VisualizationAgent** 📊
- **O que faz:** Gera código para criar gráficos interativos
- **Quando usar:** Para pedidos como:
  - "Mostre um gráfico de barras da coluna X"
  - "Crie um histograma da idade"
  - "Faça um scatter plot entre preço e tamanho"
  - "Gere um heatmap de correlação"

### 4. **ConsultantAgent** 💡
- **O que faz:** Interpreta os dados e fornece insights de negócio
- **Quando usar:** Para perguntas como:
  - "O que esses dados significam para meu negócio?"
  - "Quais são as principais descobertas?"
  - "Que decisões devo tomar baseado nestes dados?"
  - "Quais são os riscos e oportunidades?"

### 5. **CodeGeneratorAgent** ⚙️
- **O que faz:** Gera código Python completo para suas análises
- **Quando usar:** Para pedidos como:
  - "Me dê o código para esta análise"
  - "Gere um notebook Jupyter"
  - "Crie um script Python para automatizar isso"

## 🚀 Como Usar

### 1. **Instalação**

```bash
# 1. Clone o repositório
cd rhein-ai-agent-challenge

# 2. Crie um ambiente virtual
python -m venv .venv

# 3. Ative o ambiente
# Windows:
.venv\Scripts\activate
# Linux/Mac:
# 4. Instale as dependências
pip install -r requirements.txt
```toml
[custom]
google_api_key = "sua_chave_aqui"
supabase_url = "https://seu-projeto.supabase.co"
supabase_key = "sua_chave_supabase_aqui"
```

#### **Método 2: Variáveis de Ambiente**

Crie um arquivo `.env` baseado no `.env.example`:

```bash
cp .env.example .env
```

Edite o `.env` com suas chaves:
- **GOOGLE_API_KEY**: Obtenha em [Google AI Studio](https://makersuite.google.com/app/apikey)
- **SUPABASE_URL** e **SUPABASE_KEY**: Obtenha em [Supabase Dashboard](https://supabase.com/dashboard)

### 3. **Executar a Aplicação**

```bash
streamlit run app.py
```

Acesse a aplicação no navegador em `http://localhost:8501`

### 4. **Usando a Aplicação**

1. **Upload do CSV**: Arraste seu arquivo CSV para a área lateral
2. **Faça perguntas**: Digite suas perguntas em português na caixa de chat
3. **Explore sugestões**: Clique nas sugestões de perguntas que aparecem
## 💡 Exemplos Práticos

### **Exemplo 1: Análise de Vendas**
```
Dataset: vendas.csv (colunas: produto, categoria, valor, data, região)

Perguntas que você pode fazer:
- "Qual foi o produto mais vendido no último trimestre?"
- "Mostre um gráfico de barras das vendas por categoria"
- "Qual é a correlação entre valor e região?"
- "O que esses dados indicam sobre o desempenho regional?"
- "Gere o código para analisar a sazonalidade das vendas"
```

### **Exemplo 2: Análise de Recursos Humanos**
```
Dataset: funcionarios.csv (colunas: nome, idade, salario, departamento, tempo_casa)

Perguntas que você pode fazer:
- "Qual é a distribuição salarial por departamento?"
- "Crie um histograma da idade dos funcionários"
- "Quantos funcionários temos em cada departamento?"
- "Existe correlação entre tempo de casa e salário?"
- "Quais insights podemos tirar sobre retenção de talentos?"
```

### **Exemplo 3: Análise de Marketing**
```
Dataset: campanhas.csv (colunas: campanha, canal, investimento, conversoes, receita)

Perguntas que você pode fazer:
- "Qual canal de marketing tem o melhor ROI?"
- "Mostre um scatter plot entre investimento e receita"
- "O que os dados dizem sobre a efetividade das campanhas?"
- "Gere código para calcular métricas de performance"
- "Quais campanhas devemos investir mais?"
```

### **Datasets de Exemplo para Testar**

Se você não tem dados próprios, pode usar estes datasets públicos:

1. **Titanic Dataset** (sobreviventes do Titanic)
   - [Baixar CSV](https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv)

2. **Iris Dataset** (flores - dados científicos)
   - [Baixar CSV](https://raw.githubusercontent.com/uiuc-cse/data-fa14/gh-pages/data/iris.csv)

3. **Wine Quality** (avaliação de vinhos)
   - [Baixar CSV](https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv)

4. **House Prices** (preços de imóveis)
   - [Baixar CSV](https://raw.githubusercontent.com/ageron/handson-ml2/master/datasets/housing/housing.csv)

### **Obrigatórios**
- ✅ Python 3.8 ou superior
- ✅ Chave da API do Google Gemini

### **Opcionais (mas recomendados)**
- ✅ Conta no Supabase (para salvar histórico)
- ✅ Git (para controle de versão)

## 🔧 Dependências Principais

| Biblioteca | Propósito |
|------------|-----------|
| `streamlit` | Interface web da aplicação |
| `langchain` | Framework para agentes de IA |
| `google-generativeai` | Modelo de IA (Gemini) |
| `pandas` | Manipulação de dados |
| `plotly` | Criação de gráficos interativos |
| `supabase` | Banco de dados para histórico |

## 🗄️ Supabase: Script de Criação de Tabelas

Use o script abaixo para criar as tabelas no seu projeto Supabase. Você pode executar no SQL Editor do Supabase.

```sql
-- Habilita a extensão para usar UUIDs
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tabela de sessões de análise
CREATE TABLE sessions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  dataset_name TEXT,
  dataset_hash TEXT,
  user_id TEXT -- Pode ser um identificador de sessão do Streamlit
);

-- Tabela de conversas (perguntas e respostas)
CREATE TABLE conversations (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  session_id UUID REFERENCES sessions(id) ON DELETE CASCADE,
  question TEXT NOT NULL,
  answer TEXT,
  chart_json JSONB, -- Para armazenar a especificação do gráfico Plotly
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabela de análises estatísticas detalhadas
CREATE TABLE analyses (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  session_id UUID REFERENCES sessions(id) ON DELETE CASCADE,
  conversation_id UUID REFERENCES conversations(id) ON DELETE SET NULL, -- Análise pode ser associada a uma conversa
  analysis_type TEXT NOT NULL, -- Ex: 'descriptive_stats', 'correlation_matrix'
  results JSONB NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabela de conclusões e insights gerados
CREATE TABLE conclusions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  session_id UUID REFERENCES sessions(id) ON DELETE CASCADE,
  conversation_id UUID REFERENCES conversations(id) ON DELETE SET NULL,
  conclusion_text TEXT NOT NULL,
  confidence_score FLOAT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabela de códigos gerados
CREATE TABLE generated_codes (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  session_id UUID REFERENCES sessions(id) ON DELETE CASCADE,
  conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
  code_type TEXT NOT NULL, -- 'analysis', 'visualization', 'complete', 'notebook'
  python_code TEXT NOT NULL,
  description TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Adiciona índices para otimizar consultas
CREATE INDEX idx_conversations_session_id ON conversations(session_id);
CREATE INDEX idx_analyses_session_id ON analyses(session_id);
CREATE INDEX idx_conclusions_session_id ON conclusions(session_id);
CREATE INDEX idx_generated_codes_session_id ON generated_codes(session_id);
```

## 🎨 Funcionalidades Avançadas

### **Cache Inteligente**
- Os gráficos são armazenados em cache para evitar recriação desnecessária
- Melhora a performance e reduz custos com API

### **Histórico Persistente**
- Suas conversas e análises são salvas automaticamente
- Recupere sessões anteriores a qualquer momento

### **Sugestões Dinâmicas**
- A IA sugere perguntas relevantes baseadas no contexto
- Melhora a experiência de exploração dos dados

### **Execução Segura de Código**
- O código Python gerado é executado em ambiente isolado
- Previne execução de código malicioso

## 🛠️ Estrutura do Projeto

```
rhein-ai-agent-challenge/
├── agents/              # Agentes especializados de IA
│   ├── coordinator.py   # Decide qual agente usar
│   ├── data_analyst.py  # Análises estatísticas
│   ├── visualization.py # Geração de gráficos
│   ├── consultant.py    # Insights de negócio
│   └── code_generator.py # Geração de código
├── components/          # Componentes da interface
│   ├── ui_components.py # Elementos visuais
│   └── suggestion_generator.py # Sugestões inteligentes
├── utils/              # Utilitários e helpers
│   ├── config.py       # Configurações da app
│   ├── data_loader.py  # Carregamento de CSVs
│   ├── memory.py       # Integração com banco
│   └── chart_cache.py  # Cache de gráficos
├── app.py              # Arquivo principal
├── requirements.txt    # Dependências Python
└── README.md          # Este arquivo
```

## 📊 Tipos de Análise Suportados

### **Análises Estatísticas**
- Estatísticas descritivas (média, mediana, desvio padrão)
- Contagem de valores únicos e nulos
- Identificação de outliers
- Análise de correlação
- Testes de hipóteses

### **Visualizações Disponíveis**
- Histogramas e distribuições
- Gráficos de barras e colunas
- Scatter plots e dispersão
- Box plots e violin plots
- Heatmaps de correlação
- Gráficos de linha e área

### **Insights de Negócio**
- Interpretação de tendências
- Identificação de padrões
- Recomendações estratégicas
- Análise de oportunidades
- Detecção de anomalias

## 🔒 Segurança e Privacidade

- ✅ **Dados locais**: Seus arquivos CSV ficam apenas no seu computador
- ✅ **Código isolado**: Análises são executadas em ambiente seguro
- ✅ **API keys protegidas**: Configurações sensíveis são criptografadas
- ✅ **Histórico opcional**: Use Supabase apenas se quiser salvar conversas

## 🆘 Suporte e Troubleshooting

### **Problemas Comuns**

**1. "Chave da API não configurada"**
```bash
# Verifique se a chave está no arquivo .streamlit/secrets.toml
# ou nas variáveis de ambiente
```

**2. "Erro ao carregar CSV"**
- Verifique se o arquivo é um CSV válido
- Certifique-se de que tem pelo menos uma linha de dados
- Arquivos muito grandes podem precisar de mais memória

**3. "Gráfico não aparece"**
- Aguarde alguns segundos após fazer a pergunta
- Verifique se há dados suficientes para o tipo de gráfico
- Tente reformular a pergunta

### **Logs e Debug**

Para ver logs detalhados:
```python
# Execute com debug habilitado
DEBUG_MODE = True  # No arquivo app.py, linha 31
```

## ❓ FAQ - Perguntas Frequentes

### **🔑 Configuração e API**

**P: Como obter a chave da API do Google Gemini?**
```
R: Acesse https://makersuite.google.com/app/apikey
   Clique em "Create API key"
   Copie a chave gerada e configure no .streamlit/secrets.toml
```

**P: A aplicação funciona sem o Supabase?**
```
R: Sim! O Supabase é opcional e serve apenas para salvar o histórico.
   Você pode usar a aplicação normalmente sem ele.
```

## ⚠️ Limites de Taxa da API do Gemini

A aplicação utiliza a API do Google Gemini, que possui os seguintes limites na versão gratuita:

- **Limite de requisições**: 200 requisições por dia
- **Modelo padrão**: Gemini 2.0 Flash
- **Tempo de espera**: Aproximadamente 1 minuto após atingir o limite

### O que acontece quando atinjo o limite?

- Você verá uma mensagem amigável em português explicando o limite
- A aplicação continuará funcionando para análise local dos dados
- As funcionalidades que dependem da API (respostas da IA) ficarão temporariamente indisponíveis

### Como gerenciar o limite?

1. **Acompanhe seu uso**: Verifique seu consumo em [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Atualize seu plano**: Considere atualizar para um plano pago se precisar de mais requisições
3. **Aguarde**: O limite é reiniciado após 24 horas da primeira requisição

Para mais informações, consulte a [documentação oficial da API Gemini](https://ai.google.dev/gemini-api/docs/rate-limits).

---

**P: Quais são os custos da API do Google?**
```
R: O Google Gemini tem uma cota gratuita generosa.
   Para uso básico, dificilmente você gastará algo.
   Consulte: https://ai.google.dev/pricing
```

### **📊 Dados e Análises**

**P: Quais formatos de arquivo são suportados?**
```
R: Atualmente apenas arquivos CSV.
   Certifique-se de que o arquivo tem extensão .csv
   e está separado por vírgulas.
```

**P: Há limite de tamanho para os arquivos?**
```
R: Não há limite técnico, mas arquivos muito grandes (>100MB)
   podem causar lentidão. Recomendamos começar com datasets menores.
```

**P: Posso fazer perguntas em português?**
```
R: Sim! A aplicação está configurada para funcionar em português.
   Você pode fazer perguntas naturalmente em português brasileiro.
```

### **🔧 Problemas Técnicos**

**P: A aplicação não inicia. O que fazer?**
```
R: 1. Verifique se todas as dependências estão instaladas
   2. Confirme se a chave da API está configurada
   3. Tente: pip install -r requirements.txt
   4. Reinicie o ambiente virtual
```

**P: Os gráficos não aparecem. Como resolver?**
```
R: 1. Aguarde alguns segundos após fazer a pergunta
   2. Verifique se há dados suficientes para o gráfico
   3. Tente reformular a pergunta
   4. Verifique o console por erros
```

**P: As sugestões de perguntas não aparecem**
```
R: 1. Certifique-se de que há histórico de conversa
   2. Verifique se a chave da API está funcionando
   3. Tente recarregar a página
```

### **🚀 Uso Avançado**

**P: Como exportar o código gerado?**
```
R: O código aparece automaticamente na conversa.
   Você pode copiá-lo e colar em seu editor de código.
```

**P: Posso usar meus próprios modelos de IA?**
```
R: Atualmente a aplicação usa Google Gemini.
   Para outros modelos, seria necessário modificar o código.
```

**P: Como contribuir com o projeto?**
```
R: 1. Faça um fork no GitHub
   2. Crie uma branch para sua feature
   3. Teste suas mudanças
   4. Abra um Pull Request
```

### **📈 Performance**

**P: Por que a aplicação está lenta?**
```
R: 1. Datasets muito grandes podem causar lentidão
   2. Muitas perguntas simultâneas
   3. Limitações da API gratuita
   4. Hardware insuficiente
```

**P: Como melhorar a performance?**
```
R: 1. Use datasets menores para começar
   2. Faça perguntas mais específicas
   3. Aguarde entre perguntas
   4. Considere usar cache local
```

## 🔒 Limitações Conhecidas

Este é um projeto de aprendizado e exploração. Sugestões são bem-vindas!

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para detalhes.

## 🙏 Agradecimentos

- **Google Gemini** pela inteligência artificial
- **Streamlit** pela incrível framework web
- **LangChain** pela abstração de agentes
- **Plotly** pelas visualizações interativas
- **Supabase** pelo banco de dados em tempo real

---

**Desenvolvido com ❤️ para democratizar a análise de dados**
