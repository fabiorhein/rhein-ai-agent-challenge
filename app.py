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
from utils.chart_cache import exec_with_cache  # Import do cache de gráficos
from components.ui_components import build_sidebar, display_chat_message, display_code_with_streamlit_suggestion
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
            try:
                df, file_hash = load_csv(uploaded_file)
                st.session_state.df = df
                st.session_state.df_info = get_dataset_info(df, uploaded_file.name)

                # Cria uma nova sessão no Supabase
                session_id = memory.create_session(
                    dataset_name=uploaded_file.name,
                    dataset_hash=file_hash,
                    user_id=st.session_state.user_id
                )
                
                # Define o ID da sessão no estado
                st.session_state.session_id = session_id
                
                # Carrega o histórico da sessão, se existir
                try:
                    session_history = memory.get_session_history(session_id)
                    
                    # Restaura o histórico de conversas
                    if session_history["conversations"]:
                        st.session_state.conversation_history = "\n".join(
                            f"{'Usuário' if i % 2 == 0 else 'Assistente'}: {msg['question'] if i % 2 == 0 else msg['answer']}"
                            for i, msg in enumerate(session_history["conversations"])
                        )
                    
                    # Restaura as análises
                    if session_history["analyses"]:
                        st.session_state.all_analyses_history = "\n".join(
                            f"Análise: {analysis['results'].get('analysis', '')}"
                            for analysis in session_history["analyses"]
                        )
                        
                except Exception as e:
                    st.error(f"Erro ao carregar histórico da sessão: {e}")
                    st.session_state.conversation_history = ""
                    st.session_state.all_analyses_history = f"Análise iniciada para o dataset: {uploaded_file.name}\n"
                st.rerun()  # Força recarregamento para mostrar o dataset
            except ValueError as e:
                st.error(f"Erro ao carregar o arquivo: {e}")
                st.session_state.df = None
    else:
        # Dataset já carregado, não mostrar mensagem de debug
        pass

# Verificação: se não há arquivo carregado mas há dados no estado, limpar automaticamente
if uploaded_file is None and st.session_state.get('df') is not None:
    st.sidebar.info("📤 Nenhum arquivo carregado. Os dados foram limpos automaticamente.")
    # Limpar dados automaticamente
    st.session_state.df = None
    st.session_state.df_info = None
    st.session_state.session_id = None
    st.session_state.messages = []
    st.session_state.conversation_history = ""
    st.session_state.all_analyses_history = ""

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

    # Exibe mensagens do histórico (preservar mensagens existentes)
    for i, message in enumerate(st.session_state.messages):
        display_chat_message(message["role"], message["content"], message.get("chart_fig"), generated_code=message.get("generated_code"))

    # Exibir gráfico preservado apenas se ainda não estiver nas mensagens
    if 'last_chart' in st.session_state and st.session_state.last_chart:
        assistant_has_chart = any(
            message.get("role") == "assistant" and message.get("chart_fig") is not None
            for message in st.session_state.messages
        )

        if assistant_has_chart:
            # Evitar duplicação removendo o gráfico preservado redundante
            del st.session_state.last_chart
            if 'last_chart_code' in st.session_state:
                del st.session_state.last_chart_code
        else:
            st.success("📊 Gráfico preservado da análise anterior:")
            try:
                chart_key = f"preserved_chart_{len(st.session_state.messages)}"
                st.plotly_chart(st.session_state.last_chart, use_container_width=True, key=chart_key)
            except Exception as e:
                st.warning(f"⚠️ Erro ao exibir gráfico preservado: {e}")
                # Limpar gráfico preservado se houver erro
                if 'last_chart' in st.session_state:
                    del st.session_state.last_chart

    # --- Sugestões Dinâmicas de Perguntas ---
    st.subheader("Sugestões de Perguntas:")

    # Sempre gerar sugestões baseadas no histórico atual
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

            # Gerar novas sugestões sempre com o histórico atualizado
            suggestions = generate_dynamic_suggestions(
                api_key=config["google_api_key"],
                dataset_preview=dataset_preview,
                conversation_history=enriched_history
            )

        except Exception as e:
            st.error(f"❌ **Erro ao gerar sugestões:** {e}")
            suggestions = get_fallback_suggestions()
            st.warning(f"📝 **Usando sugestões padrão:** {len(suggestions)} sugestões")
    else:
        # Se não há histórico, usar sugestões padrão
        suggestions = get_fallback_suggestions()

    # Garantir que sempre tenhamos sugestões
    if not suggestions:
        suggestions = get_fallback_suggestions()
        st.error("⚠️ **Fallback ativado: usando sugestões padrão**")

    # Exibir as sugestões
    st.write(f"🔍 **Mostrando {len(suggestions[:3])} sugestões:**")
    cols = st.columns(3)
    for i, suggestion in enumerate(suggestions[:3]):
        if cols[i].button(suggestion, use_container_width=True, key=f"suggestion_{i}"):
            st.session_state.last_question = suggestion

    if prompt := st.chat_input("Faça sua pergunta sobre os dados...") or st.session_state.get('last_question'):
        st.session_state.last_question = None  # Limpa a sugestão imediatamente

        # Adiciona a pergunta do usuário ao histórico e exibe
        st.session_state.messages.append({"role": "user", "content": prompt})
        display_chat_message("user", prompt)

        # Adiciona ao histórico de texto para os agentes
        st.session_state.conversation_history += f"Usuário: {prompt}\n"
        
        # Inicializa conversation_id como None
        conversation_id = None
        
        # Registrar a conversa no banco de dados
        if st.session_state.session_id:
            try:
                conversation_id = memory.log_conversation(
                    session_id=st.session_state.session_id,
                    question=prompt,
                    answer=""  # A resposta será atualizada quando estiver pronta
                )
            except Exception as e:
                st.error(f"Erro ao registrar conversa: {e}")

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
                
                # Inicializa conversation_id como None
                conversation_id = None

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
                    
                    # Armazenar a análise no banco de dados
                    if st.session_state.session_id:
                        try:
                            memory.store_analysis(
                                session_id=st.session_state.session_id,
                                conversation_id=conversation_id,
                                analysis_type="data_analysis",
                                results={"analysis": bot_response_content}
                            )
                        except Exception as e:
                            st.error(f"Erro ao salvar análise: {e}")

                elif agent_to_call == "VisualizationAgent":
                    try:
                        generated_code = run_visualization(
                            api_key=config["google_api_key"],
                            df=st.session_state.df,
                            analysis_results=st.session_state.all_analyses_history,
                            user_request=question_for_agent
                        )

                        # Tenta executar o código para gerar o gráfico usando cache
                        try:
                            # Usar cache otimizado para gráficos
                            chart_figure = exec_with_cache(generated_code, st.session_state.df)

                            if chart_figure:
                                bot_response_content = "Aqui está a visualização que você pediu."
                                st.session_state.all_analyses_history += f"Visualização Gerada: {question_for_agent}\n"
                            else:
                                bot_response_content = "O código foi gerado, mas não criou uma figura válida. Verifique se o código define uma variável 'fig'."
                        except SyntaxError as se:
                            bot_response_content = f"Erro de sintaxe no código gerado: {se}\n\nCódigo com erro:\n```python\n{generated_code}\n```"
                        except NameError as ne:
                            bot_response_content = f"Erro: variável não definida no código: {ne}\n\nCódigo com erro:\n```python\n{generated_code}\n```"
                        except Exception as e:
                            bot_response_content = f"Erro ao executar código do gráfico: {e}\n\nCódigo que falhou:\n```python\n{generated_code}\n```"

                    except Exception as e:
                        bot_response_content = f"Erro no agente de visualização: {e}\n\nTente reformular sua pergunta ou verifique se sua chave da API do Google está configurada corretamente."

                elif agent_to_call == "ConsultantAgent":
                    bot_response_content = run_consultant(
                        api_key=config["google_api_key"],
                        df=st.session_state.df,
                        all_analyses=st.session_state.all_analyses_history,
                        user_question=question_for_agent
                    )
                    
                    # Armazenar a conclusão no banco de dados
                    if st.session_state.session_id:
                        try:
                            memory.store_conclusion(
                                session_id=st.session_state.session_id,
                                conversation_id=conversation_id,
                                conclusion_text=bot_response_content,
                                confidence_score=0.9  # Pontuação de confiança padrão
                            )
                        except Exception as e:
                            st.error(f"Erro ao salvar conclusão: {e}")

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

                # Executar código automaticamente se foi gerado
                if generated_code:
                    # Exibir código com containers para execução
                    with st.chat_message("assistant"):
                        st.markdown(bot_response_content)

                        # Sempre exibir o código gerado PRIMEIRO
                        execution_container, results_container = display_code_with_streamlit_suggestion(generated_code, auto_execute=True)

                        # Exibir gráfico APENAS se foi gerado pelo VisualizationAgent (evita duplicação)
                        if chart_figure and agent_to_call == "VisualizationAgent":
                            try:
                                # Usar chave única para evitar re-renderização
                                chart_key = f"chart_{len(st.session_state.messages)}_{hash(str(chart_figure))}"
                                st.plotly_chart(chart_figure, use_container_width=True, key=chart_key)
                            except Exception as e:
                                st.warning(f"⚠️ Erro ao exibir gráfico na execução inicial: {str(e)}")

                    # Atualizar a mensagem no histórico com verificação robusta
                    chart_to_save = chart_figure
                    if chart_figure:
                        try:
                            # Verificar se o gráfico é serializável
                            chart_figure.to_json()
                        except Exception as e:
                            # Manter o gráfico mesmo se não for serializável
                            pass

                    # Remover deep copy para melhorar performance
                    # chart_to_save = copy.deepcopy(chart_to_save) se necessário

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": bot_response_content,
                        "chart_fig": chart_to_save,
                        "generated_code": generated_code
                    })

                    if execution_container is None:
                        st.error("❌ Erro: Containers não foram criados corretamente!")
                        # Não usar return aqui, continuar a execução

                    # Executar o código gerado (apenas para CodeGeneratorAgent)
                    if agent_to_call == "CodeGeneratorAgent":
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
                                results_container.markdown("**Erro:** Nenhum arquivo CSV foi carregado.")
                                st.error("Erro: Nenhum DataFrame disponível para análise.")
                                # Não usar return, continuar com o fluxo

                            # Executar o código usando cache otimizado
                            exec_with_cache(generated_code, local_scope)

                            # Verificar se foi gerada uma figura
                            if 'fig' in local_scope:
                                execution_container.markdown("**Status:** ✅ Código executado com sucesso!")
                                results_container.markdown("**Resultados:** Visualização gerada automaticamente:")

                                # Exibir a figura gerada APENAS UMA VEZ
                                fig = local_scope['fig']
                                # Usar chave única para evitar re-renderização
                                fig_key = f"code_chart_{len(st.session_state.messages)}_{id(fig)}"
                                st.plotly_chart(fig, use_container_width=True, key=fig_key)

                                # Atualizar a mensagem para incluir a figura
                                st.session_state.messages[-1]["chart_fig"] = fig
                                chart_figure = fig

                            else:
                                execution_container.markdown("**Status:** ✅ Código executado com sucesso!")
                                results_container.markdown("**Resultados:** Código executado sem gerar visualização específica.")

                            # Capturar outras saídas importantes
                            if 'result' in local_scope:
                                results_container.markdown(f"**Valor de retorno:** {local_scope['result']}")
                        except Exception as e:
                            execution_container.markdown(f"**Status:** ❌ Erro na execução: {str(e)}")
                            results_container.markdown(f"**Detalhes do erro:** {str(e)}")
                            st.error(f"Erro na execução do código: {e}")
                    else:
                        # Para VisualizationAgent, mostrar que o código já foi executado
                        if execution_container and results_container:
                            execution_container.markdown("**Status:** ✅ Código executado com sucesso!")
                            results_container.markdown("**Resultados:** Gráfico gerado automaticamente acima.")

                else:
                    # Para agentes sem código, usar display_chat_message normalmente
                    display_chat_message("assistant", bot_response_content, chart_figure, generated_code=None)

                    # Atualizar a mensagem no histórico
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": bot_response_content,
                        "chart_fig": chart_figure,
                        "generated_code": None
                    })

                # Atualiza o histórico de texto APÓS processar a resposta
                st.session_state.conversation_history += f"Assistente: {bot_response_content}\n"

                # Forçar atualização das sugestões na próxima renderização
                st.session_state.suggestions = []  # Forçar regeneração

                # 4. Salva no Supabase
                try:
                    chart_json = None
                    if chart_figure:
                        try:
                            # Converter gráfico para JSON com timeout protection
                            chart_json = chart_figure.to_json()
                            # Se o JSON for muito grande, truncar para evitar timeout
                            if len(chart_json) > 10000:  # Reduzir limite para ~10KB
                                chart_json = chart_json[:10000] + "\n... (truncado para evitar timeout)"
                        except Exception as json_error:
                            # Se não conseguir converter, salvar apenas metadados básicos
                            st.warning(f"⚠️ Não foi possível converter gráfico para JSON: {str(json_error)}")
                            chart_json = f"Gráfico gerado ({type(chart_figure).__name__})"

                    # Inicializa a variável conv_id
                    conv_id = None
                    # Atualizar a conversa existente em vez de criar uma nova
                    if 'conversation_id' in locals() and conversation_id:
                        try:
                            # Atualiza a conversa existente
                            memory.client.table("conversations").update({
                                "answer": bot_response_content,
                                "chart_json": chart_json
                            }).eq("id", conversation_id).execute()
                            conv_id = conversation_id
                        except Exception as e:
                            st.error(f"Erro ao atualizar conversa: {e}")
                    else:
                        # Se não tiver um ID de conversa, cria uma nova
                        try:
                            # Cria uma nova conversa e pega o ID retornado
                            conv_response = memory.log_conversation(
                                session_id=st.session_state.session_id,
                                question=prompt,
                                answer=bot_response_content,
                                chart_json=chart_json
                            )
                            conv_id = conv_response  # Atribui o ID retornado
                        except Exception as e:
                            st.error(f"Erro ao salvar conversa: {e}")
                except Exception as db_error:
                    st.warning(f"⚠️ Erro ao salvar conversa no banco: {str(db_error)}")
                    conv_id = None

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

                # Recarregar a página para atualizar as sugestões com o novo histórico
                # Mas apenas se estivermos em modo debug OU se não houver gráfico para evitar problemas
                should_rerun = False  # Otimização: reduzir reruns desnecessários

                if chart_figure:
                    # Se há gráfico, só fazer rerun em modo debug para evitar problemas de renderização
                    if DEBUG_MODE:
                        st.success("✅ Resposta processada com sucesso! (Gráfico preservado - rerun em modo debug)")
                        should_rerun = True
                    else:
                        st.success("✅ Resposta processada com sucesso!")
                        should_rerun = False
                else:
                    # Se não há gráfico, rerun é seguro
                    if DEBUG_MODE:
                        st.success("✅ Resposta processada com sucesso! (Sem gráfico - rerun em modo debug)")
                    else:
                        st.success("✅ Resposta processada com sucesso!")
                    should_rerun = False  # Otimização: evitar rerun desnecessário

                if should_rerun and DEBUG_MODE:
                    st.rerun()

                # FORÇAR ATUALIZAÇÃO DAS SUGESTÕES APÓS CADA RESPOSTA
                st.info("🔄 Atualizando sugestões com o novo contexto...")

                # Preservar gráficos antes do re-run apenas se necessário
                if chart_figure:
                    st.session_state.last_chart = chart_figure
                    st.session_state.last_chart_code = generated_code

                # Forçar re-run para atualizar sugestões com o novo contexto
                # Mas apenas se não estivermos em modo debug para evitar problemas
                if not DEBUG_MODE:
                    time.sleep(0.5)  # Pequena pausa para mostrar a mensagem
                    st.rerun()
                else:
                    st.success("✅ Sugestões atualizadas (modo debug - sem re-run)")

                # Limpar gráficos preservados após o re-run bem-sucedido
                if 'last_chart' in st.session_state:
                    del st.session_state.last_chart
                if 'last_chart_code' in st.session_state:
                    del st.session_state.last_chart_code

            except Exception as e:
                st.error(f"Ocorreu um erro inesperado: {e}")

# Adiciona um footer
st.markdown("---")
st.markdown("Sistema de Análise Exploratória de Dados com IA - Projeto Acadêmico")