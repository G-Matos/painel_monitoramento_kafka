from modules.requestsClass import HttpRequests, SetConnector
import streamlit as st
from streamlit_autorefresh import st_autorefresh # type: ignore
#from user_login_panel.controllers.user_controller import UserController
from modules.dataLog import *
from config import kafka_ports

st.logo("static/new-linkedby.png")
st.set_page_config(layout="wide")
st.header("Monitoramento Conectores Kafka",divider="red")

def main():
    #controle de login 
    #user_controller = UserController()
    #user_view = user_controller.handle_main_page()
    #if user_controller.get_logged_in():
    #    start_date_str = user_view.get_start_date().strftime('%Y-%m-%d')
    #    end_date_str = user_view.get_end_date().strftime('%Y-%m-%d')
    #    # Obtém as permissões e exceções do user_controller
    #    permission_filter = [user_controller.get_permition()] if user_controller.get_permition() else []
    #    exception_filter = [user_controller.get_exception()] if user_controller.get_exception() else []
    
    connector_info = HttpRequests.connector_info()
    sink_df = connector_info[(connector_info["Type"] == "sink") & 
                         (~connector_info["Conector"].str.contains("envio", na=False))]
    source_df = connector_info[connector_info["Type"] == "source"]
    paused_df = connector_info[connector_info["Status Atual"] == "PAUSED"]
    failed_df = connector_info[connector_info["Status Atual"] == "FAILED"]
    octopus_df = connector_info[connector_info["Conector"].str.contains("envio", case=False)]

    with st.sidebar:
        st.subheader("Sincronizar dados dos Conectores", divider="blue")
        with st.expander("Sincronismo"):
            st.info("Utilize apenas quando for necessário ober novos conectores incluidos.")
            if st.button("Sincronizar", type="primary", use_container_width=True):
                SetConnector.get_connector(kafka_ports)
                print("Informações Sincronizadas!")

    # visualiação geral (contadores)
    st.subheader("Visualização Geral")

    with st.container(border=True):
        info1, info2, info3, info4 = st.columns(4)
    with info1:
        st.write(f'Conectores monitorados: :green[{connector_info["Conector"].count()}]')
    with info2:
        status_ok = connector_info[connector_info["Status Atual"] == "RUNNING"]
        st.write(f'Conectores com status RUNNIG: :green[{status_ok["Conector"].count()}]')
    with info3:
        st.write(f'Conectores com status FAILED: :red[{failed_df["Conector"].count()}]')
    with info4:
        st.write(f'Conectoes com status PAUSED: :red[{paused_df["Conector"].count()}]')

    # Alertas de conectores 
    Warning1 = connector_info.loc[connector_info['Status Atual'] == "PAUSED"]
    Warning2 = connector_info.loc[connector_info['Status Atual'] == "FAILED"]
    # aba de status dos conectores
    status_conn, error_conn = st.tabs(["Status Conectores", "Alerta de Conectores"])

    with status_conn:
        if not Warning1.empty:
            log_writer = LogWrite() 
            log_writer.log_write(Warning1.values, "paused")
            st.warning('Conectores com status "PAUSED" identificados', icon="⚠️")
        if not Warning2.empty:
            log_writer = LogWrite() 
            log_writer.log_write(Warning2.values, "failed")
            st.error('Conectores com status "FAILED" identificados', icon="🚨")

        sink_column, source_column = st.columns(2)
        with sink_column:
            st.subheader("Conectores Sink")
            st.dataframe(sink_df, hide_index=True, use_container_width=True)
        with source_column:
            st.subheader("Conectores Source")
            st.dataframe(source_df, hide_index=True, use_container_width=True)
        st.divider()
        st.subheader(" Conectores Sink Octopus")
        with st.container(border=False):
            st.dataframe(octopus_df, hide_index=True, use_container_width=True)

    # Aba de alerta dos conectores
    with error_conn: 
        
        st.subheader("Alerta de Conectores em Pausa")
        with st.container(border=False):
            if not paused_df.empty:
                st.dataframe(paused_df, hide_index=True, use_container_width=True)
            else:
                st.info('Nenhum conector com status :red[Paused] encontrado.', icon="ℹ️")
        st.divider()
        st.subheader("Alerta de Conectores com Falha")
        with st.container(border=False):
            if not failed_df.empty:
                st.dataframe(failed_df, hide_index=True, use_container_width=True)
            else:
                st.info('Nenhum conector com status :red[FAILED] encontrado.', icon="ℹ️")
        
        st_autorefresh(interval=300000, key="refresh")
    
    footer = """
            <style>
                .footer {
                    position: static;
                    bottom: 0;
                    left: 0;  /* Garante que o rodapé esteja alinhado à esquerda */
                    width: 100%;
                    background-color: rgb(14, 17, 23);
                    text-align: center;  /* Centraliza o texto dentro do rodapé */
                    padding: 10px;
                    font-size: 14px;
                    color: white;  /* Adicionando uma cor de texto para facilitar a leitura */
                }
            </style>

            <div class="footer">
                <p>2025 Painel Monitoramento Kafka | v 1.1.2 by Gabriel Matos ®</p>
            </div>
        """
    st.divider()
    st.markdown(footer, unsafe_allow_html=True)

if __name__ == "__main__":
    main()