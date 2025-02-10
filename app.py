import streamlit as st
from request import get_status_sink, get_status_source
import pandas as pd
from streamlit_autorefresh import st_autorefresh # type: ignore
#from user_login_panel.controllers.user_controller import UserController

#Config pagina
#st.logo("static/new-linkedby.png")
st.set_page_config(layout="wide")
st.header("Monitoramento Conectores Kafka",divider="gray")

def main():
    #user_controller = UserController()
    #user_view = user_controller.handle_main_page()
    #if user_controller.get_logged_in():
    #    start_date_str = user_view.get_start_date().strftime('%Y-%m-%d')
    #    end_date_str = user_view.get_end_date().strftime('%Y-%m-%d')
    #    # Obtém as permissões e exceções do user_controller
    #    permission_filter = [user_controller.get_permition()] if user_controller.get_permition() else []
    #    exception_filter = [user_controller.get_exception()] if user_controller.get_exception() else []
    
        #sink data
        sink_tab = get_status_sink()
        if not sink_tab:
            sink_df = pd.DataFrame()
        else:
            sink_df = pd.DataFrame(sink_tab).sort_values(by='Status Atual', key=lambda x: x.strip() != 'PAUSED')
        
        #source data
        source_tab = get_status_source()
        if source_tab.empty:
            source_df = pd.DataFrame()
        else:
            source_df = pd.DataFrame(source_tab).sort_values(by='Status Atual', key=lambda x: x != 'PAUSED')

        combined_df = pd.concat([sink_df, source_df])
        paused_df = combined_df[combined_df["Status Atual"] == "PAUSED"]
        failed_df = combined_df[combined_df["Status Atual"] == "FAILED"]

        st.subheader("Visualização Geral")
        with st.container(border=True):
            info1, info2, info3, info4 = st.columns(4)
            with info1:
                st.write(f'Conectores monitorados: :green[{combined_df["Conector"].count()}]')
            with info2:
                status_ok = combined_df[combined_df["Status Atual"] == "RUNNING"]
                st.write(f'Conectores com status RUNNIG: :green[{status_ok["Conector"].count()}]')
            with info3:
                st.write(f'Conectores com status FAILED: :red[{failed_df["Conector"].count()}]')
            with info4:
                st.write(f'Conectoes com status PAUSED: :red[{paused_df["Conector"].count()}]')

        Warning1 = combined_df.loc[combined_df['Status Atual'] == "PAUSED"]
        Warning2 = combined_df.loc[combined_df['Status Atual'] == "FAILED"]
        
        if not Warning1.empty:
            st.warning('Conectores com status "PAUSED" identificados', icon="⚠️")
        if not Warning2.empty:
            st.warning('Conectores com status "FAILED" identificados', icon="⚠️")

        tab_status, tab_paused, tab_failed = st.tabs(["Status Conectores", "Conectores Pausados", "Conectores com Falha"])

        # Status Conectores
        with tab_status:
            sink_column, source_column = st.columns(2)
            with sink_column:
                st.subheader("Conectores Sink")
                st.dataframe(sink_df, hide_index=True)
            with source_column:
                st.subheader("Conectores Source")
                st.dataframe(source_df, hide_index=True)

         # Paused Conectores 
        with tab_paused:
            if not paused_df.empty:
                st.dataframe(paused_df, hide_index=True)
            else:
                st.write('Nenhum conector com status :red[PAUSED] encontrado!')

        # Failed Conectores
        with tab_failed:
            if not failed_df.empty:
                st.dataframe(failed_df, hide_index=True)
            else:
                st.write('Nenhum conector com status :red[FAILED] encontrado !')

        st_autorefresh(interval=300000, key="refresh")

# Execução do programa
if __name__ == "__main__":
    main()