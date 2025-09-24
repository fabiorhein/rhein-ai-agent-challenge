import streamlit as st
import pandas as pd
import time


def build_sidebar(memory, user_id):
    """Constrói a sidebar do aplicativo."""
    with st.sidebar:
        st.header("Análise EDA com IA")

        # Key única baseada no user_id para manter consistência
        unique_key = f"file_uploader_{user_id}"

        uploaded_file = st.file_uploader(
            "Faça o upload do seu arquivo CSV",
            type=["csv"],
            accept_multiple_files=False,
            key=unique_key
        )

        st.subheader("Histórico de Sessões")
        sessions = memory.get_user_sessions(user_id)
        if sessions:
            for session in sessions:
                st.info(
                    f"ID: ...{session['id'][-6:]}\nDataset: {session['dataset_name']}\nData: {pd.to_datetime(session['created_at']).strftime('%d/%m/%Y %H:%M')}")
        else:
            st.write("Nenhuma sessão anterior encontrada.")

        st.subheader("Configurações")
        st.info("Configurações futuras aqui.")

    return uploaded_file


def display_chat_message(role, content, chart_fig=None, key=None):
    """Exibe uma mensagem no chat."""
    with st.chat_message(role):
        st.markdown(content)
        if chart_fig:
            st.plotly_chart(chart_fig, use_container_width=True, key=key)