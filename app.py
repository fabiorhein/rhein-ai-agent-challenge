import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px  # Necessário para o exec
import matplotlib.pyplot as plt
import numpy as np
from uuid import uuid4
import time

# Importações dos módulos do projeto
from utils.config import get_config
from utils.memory import SupabaseMemory
from utils.data_loader import load_csv, get_dataset_info
from components.ui_components import build_sidebar, display_chat_message
from components.notebook_generator import create_jupyter_notebook
from components.suggestion_generator import generate_dynamic_suggestions, get_fallback_suggestions, extract_conversation_context

# Importação dos agentes
from agents.coordinator import run_coordinator
from agents.data_analyst import run_data_analyst
from agents.visualization import run_visualization
from agents.consultant import run_consultant
from agents.code_generator import run_code_generator
from agents.agent_setup import get_dataset_preview

# --- Configuração da Página e Estado da Sessão ---
st.set_page_config(layout="wide", page_title="InsightAgent EDA")

# Configuração de debug (pode ser alterada para False em produção)
DEBUG_MODE = False

# Inicializa o estado da sessão
if 'session_id' not in st.session_state:
    st.session_state.session_id = None
if 'user_id' not in st.session_state:
    st.session_state.user_id = str(uuid4())
if 'df' not in st.session_state:
    st.session_state.df = None
if 'df_info' not in st.session_state:
    st.session_state.df_info = None
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = ""
if 'all_analyses_history' not in st.session_state:
    st.session_state.all_analyses_history = ""

# --- Carregamento de Configurações e Serviços ---
config = get_config()

# Verificar se a chave da API está configurada
if not config["google_api_key"]:
    st.error("❌ Chave da API do Google não configurada. Por favor, configure a variável de ambiente GOOGLE_API_KEY no arquivo .env")
    st.stop()

# Verificar se as configurações do Supabase estão configuradas
if not config["supabase_url"] or not config["supabase_key"]:
    st.warning("⚠️ Configurações do Supabase não encontradas. Algumas funcionalidades podem não funcionar. Configure SUPABASE_URL e SUPABASE_KEY no arquivo .env")

memory = SupabaseMemory(url=config["supabase_url"], key=config["supabase_key"])

# --- Interface do Usuário (Sidebar) ---
uploaded_file = build_sidebar(memory, st.session_state.user_id)

# --- Lógica Principal de Processamento do CSV ---
if uploaded_file is not None:
    st.sidebar.success("Arquivo CSV carregado com sucesso!")
    if st.session_state.df is None:
        with st.spinner("Processando seu CSV... Isso pode levar um momento."):
            try:
                # Debug: mostrar informações do arquivo
                st.sidebar.write(f"**Debug - Nome do arquivo:** {uploaded_file.name}")
                st.sidebar.write(f"**Debug - Tamanho do arquivo:** {uploaded_file.size} bytes")

                df, file_hash = load_csv(uploaded_file)
                st.session_state.df = df
                st.session_state.df_info = get_dataset_info(df, uploaded_file.name)

                # Debug: mostrar informações do dataframe
                st.sidebar.write(f"**Debug - Shape do DataFrame:** {df.shape}")
                st.sidebar.write(f"**Debug - Colunas:** {list(df.columns)}")

                # Cria uma nova sessão no Supabase
                session_id = memory.create_session(
                    dataset_name=uploaded_file.name,
                    dataset_hash=file_hash,
                    user_id=st.session_state.user_id
                )
                st.session_state.session_id = session_id
                st.session_state.messages = []
                st.session_state.conversation_history = ""
                st.session_state.all_analyses_history = f"Análise iniciada para o dataset: {uploaded_file.name}\n"
                st.success("Dataset carregado com sucesso! Pronto para suas perguntas.")
                st.rerun()  # Força recarregamento para mostrar o dataset
            except ValueError as e:
                st.error(f"Erro ao carregar o arquivo: {e}")
                st.session_state.df = None
    else:
        st.sidebar.info("Dataset já carregado. Faça suas perguntas na área principal.")

# --- Área Principal de Exibição ---
st.title("🤖 InsightAgent EDA: Seu Assistente de Análise de Dados")
st.markdown("Faça o upload de um arquivo CSV na barra lateral para começar a explorar seus dados.")

if st.session_state.df is not None:
    st.header("Preview do Dataset")
    st.dataframe(st.session_state.df.head())

    st.header("Estatísticas Rápidas")
    st.json(st.session_state.df_info, expanded=False)

    # --- Interface de Chat ---
    st.header("Converse com seus Dados")

    # Exibe mensagens do histórico
    for message in st.session_state.messages:
        display_chat_message(message["role"], message["content"], message.get("chart_fig"))

    # --- Sugestões Dinâmicas de Perguntas ---
    st.subheader("Sugestões de Perguntas:")

    # Gerar sugestões baseadas no histórico da conversa ATUAL
    if st.session_state.conversation_history.strip():
        try:
            dataset_preview = get_dataset_preview(st.session_state.df)

            # Extrair contexto da conversa para melhorar as sugestões
            conversation_context = extract_conversation_context(st.session_state.conversation_history)

            # Adicionar contexto ao histórico para o agente
            enriched_history = st.session_state.conversation_history
            if conversation_context["analysis_types"]:
                enriched_history += f"\n\nTipos de análise realizados: {', '.join(conversation_context['analysis_types'])}"
            if conversation_context["agents_used"]:
                enriched_history += f"\nAgentes utilizados: {', '.join(conversation_context['agents_used'])}"

            suggestions = generate_dynamic_suggestions(
                api_key=config["google_api_key"],
                dataset_preview=dataset_preview,
                conversation_history=enriched_history
            )

            # Debug: mostrar contexto extraído (apenas em modo debug)
            if DEBUG_MODE:
                st.write("**Debug - Contexto da conversa:**")
                st.json(conversation_context)

        except Exception as e:
            st.warning(f"Erro ao gerar sugestões dinâmicas: {e}")
            suggestions = get_fallback_suggestions()
    else:
        # Se não há histórico, usar sugestões padrão
        suggestions = get_fallback_suggestions()

    # Exibir apenas as primeiras 3 sugestões
    cols = st.columns(3)
    for i, suggestion in enumerate(suggestions[:3]):
        if cols[i].button(suggestion, use_container_width=True):
            st.session_state.last_question = suggestion

    if prompt := st.chat_input("Faça sua pergunta sobre os dados...") or st.session_state.get('last_question'):
        st.session_state.last_question = None  # Limpa a sugestão

        # Adiciona a pergunta do usuário ao histórico e exibe
        st.session_state.messages.append({"role": "user", "content": prompt})
        display_chat_message("user", prompt)

        # Adiciona ao histórico de texto para os agentes
        st.session_state.conversation_history += f"Usuário: {prompt}\n"

        with st.spinner("Analisando e gerando resposta..."):
            try:
                # 1. CoordinatorAgent decide o que fazer
                coordinator_decision = run_coordinator(
                    api_key=config["google_api_key"],
                    df=st.session_state.df,
                    conversation_history=st.session_state.conversation_history,
                    user_question=prompt
                )

                agent_to_call = coordinator_decision.get("agent_to_call")
                question_for_agent = coordinator_decision.get("question_for_agent")

                st.info(f"Roteando para: **{agent_to_call}**")
                time.sleep(1)

                bot_response_content = ""
                chart_figure = None
                generated_code = ""

                # 2. Roteia para o agente apropriado
                if agent_to_call == "DataAnalystAgent":
                    bot_response_content = run_data_analyst(
                        api_key=config["google_api_key"],
                        df=st.session_state.df,
                        analysis_context=st.session_state.all_analyses_history,
                        specific_question=question_for_agent
                    )
                    st.session_state.all_analyses_history += f"Análise Estatística:\n{bot_response_content}\n"

                elif agent_to_call == "VisualizationAgent":
                    try:
                        generated_code = run_visualization(
                            api_key=config["google_api_key"],
                            df=st.session_state.df,
                            analysis_results=st.session_state.all_analyses_history,
                            user_request=question_for_agent
                        )

                        # Tenta executar o código para gerar o gráfico
                        try:
                            # Cuidado: exec é poderoso. Usar com cautela.
                            local_scope = {"df": st.session_state.df, "pd": pd, "px": px, "go": go}
                            exec(generated_code, local_scope)
                            chart_figure = local_scope.get('fig')

                            if chart_figure:
                                bot_response_content = "Aqui está a visualização que você pediu."
                                st.session_state.all_analyses_history += f"Visualização Gerada: {question_for_agent}\n"
                            else:
                                bot_response_content = "O código foi gerado, mas não criou uma figura válida. Verifique se o código define uma variável 'fig'."
                        except Exception as e:
                            bot_response_content = f"Desculpe, não consegui executar o código do gráfico. Erro: {e}\n\nCódigo que tentei executar:\n```python\n{generated_code}\n```"

                    except Exception as e:
                        bot_response_content = f"Desculpe, não consegui gerar o gráfico devido a um erro no agente de visualização: {e}\n\nTente reformular sua pergunta ou verifique se sua chave da API do Google está configurada corretamente."

                elif agent_to_call == "ConsultantAgent":
                    bot_response_content = run_consultant(
                        api_key=config["google_api_key"],
                        df=st.session_state.df,
                        all_analyses=st.session_state.all_analyses_history,
                        user_question=question_for_agent
                    )

                elif agent_to_call == "CodeGeneratorAgent":
                    analysis_context = f"Pergunta do usuário: {prompt}\n\nContexto da conversa:\n{st.session_state.all_analyses_history}"
                    generated_code = run_code_generator(
                        api_key=config["google_api_key"],
                        dataset_info=str(st.session_state.df_info),
                        analysis_to_convert=analysis_context
                    )
                    # Não incluir o código na resposta - ele será exibido automaticamente na interface
                    bot_response_content = "💡 Código Gerado: Este código será executado automaticamente na própria interface!"

                else:
                    bot_response_content = "Desculpe, não entendi qual agente usar. Poderia reformular sua pergunta?"

                # 3. Exibe a resposta do bot
                execution_container = None
                results_container = None

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": bot_response_content,
                    "chart_fig": chart_figure,
                    "generated_code": generated_code if generated_code else None
                })

                # Executar código automaticamente se foi gerado
                if generated_code:
                    if DEBUG_MODE:
                        st.write("🔍 DEBUG: Código detectado, iniciando execução...")

                    # Capturar containers para execução
                    execution_container, results_container = display_chat_message("assistant", bot_response_content, chart_figure, generated_code=generated_code)

                    if execution_container is None:
                        st.error("❌ Erro: Containers não foram criados corretamente!")
                        # Não usar return aqui, continuar a execução

                    # Executar o código gerado
                    try:
                        execution_container.markdown("**Status:** 🔄 Executando código Python gerado...")

                        # Criar ambiente seguro para execução
                        local_scope = {
                            "df": st.session_state.df,
                            "pd": pd,
                            "px": px,
                            "go": go,
                            "st": st,
                            "plt": plt,
                            "np": np
                        }

                        # Verificar se o DataFrame está disponível
                        if st.session_state.df is None:
                            execution_container.markdown("**Status:** ❌ Erro: DataFrame não encontrado!")
                            results_container.markdown("**Erro:** Nenhum arquivo CSV foi carregado.")
                            st.error("Erro: Nenhum DataFrame disponível para análise.")
                            # Não usar return, continuar com o fluxo

                        if DEBUG_MODE:
                            st.write("🔍 DEBUG: Ambiente de execução criado, executando código...")

                        # Executar o código
                        exec(generated_code, local_scope)

                        if DEBUG_MODE:
                            st.write("🔍 DEBUG: Código executado, verificando resultados...")

                        # Verificar se foi gerada uma figura
                        if 'fig' in local_scope:
                            execution_container.markdown("**Status:** ✅ Código executado com sucesso!")
                            results_container.markdown("**Resultados:** Visualização gerada automaticamente:")

                            # Exibir a figura gerada
                            fig = local_scope['fig']
                            st.plotly_chart(fig, use_container_width=True)

                            # Atualizar a mensagem para incluir a figura
                            st.session_state.messages[-1]["chart_fig"] = fig
                            chart_figure = fig

                            if DEBUG_MODE:
                                st.write("🔍 DEBUG: Figura gerada e exibida com sucesso!")

                        else:
                            execution_container.markdown("**Status:** ✅ Código executado com sucesso!")
                            results_container.markdown("**Resultados:** Código executado sem gerar visualização específica.")

                            if DEBUG_MODE:
                                st.write("🔍 DEBUG: Código executado sem gerar figura!")

                        # Capturar outras saídas importantes
                        if 'result' in local_scope:
                            results_container.markdown(f"**Valor de retorno:** {local_scope['result']}")

                    except Exception as e:
                        execution_container.markdown(f"**Status:** ❌ Erro na execução: {str(e)}")
                        results_container.markdown(f"**Detalhes do erro:** {str(e)}")
                        st.error(f"Erro na execução do código: {e}")

                else:
                    if DEBUG_MODE:
                        st.write("🔍 DEBUG: Nenhum código gerado, exibindo mensagem normal...")
                    display_chat_message("assistant", bot_response_content, chart_figure, generated_code=generated_code)

                # Atualiza o histórico de texto APÓS processar a resposta
                st.session_state.conversation_history += f"Assistente: {bot_response_content}\n"

                # 4. Salva no Supabase
                conv_id = memory.log_conversation(
                    session_id=st.session_state.session_id,
                    question=prompt,
                    answer=bot_response_content,
                    chart_json=chart_figure.to_json() if chart_figure else None
                )

                if generated_code:
                    # Tentar salvar o código gerado, mas com proteção contra timeout
                    try:
                        # Verificar se o código é muito longo (limite de 5000 caracteres)
                        if len(generated_code) > 5000:
                            # Truncar o código para evitar timeout
                            truncated_code = generated_code[:5000] + "\n\n# ... (código truncado para evitar timeout no banco de dados)"
                            code_to_save = truncated_code
                        else:
                            code_to_save = generated_code

                        memory.store_generated_code(
                            session_id=st.session_state.session_id,
                            conversation_id=conv_id,
                            code_type='visualization' if agent_to_call == "VisualizationAgent" else 'analysis',
                            python_code=code_to_save,
                            description=question_for_agent
                        )
                    except Exception as db_error:
                        # Se houver erro no banco, apenas logar e continuar
                        st.warning(f"⚠️ Código executado com sucesso, mas houve problema ao salvar: {str(db_error)}")
                        # Não interromper o fluxo principal

                # Sempre recarregar a página para atualizar as sugestões com o novo histórico
                st.rerun()

            except Exception as e:
                st.error(f"Ocorreu um erro inesperado: {e}")

# Adiciona um footer
st.markdown("---")
st.markdown("Sistema de Análise Exploratória de Dados com IA - Projeto Acadêmico")