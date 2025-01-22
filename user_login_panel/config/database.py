import streamlit as st

def get_db_url():
    return "postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}".format(
        user=st.secrets.USER_DB.user,
        password=st.secrets.USER_DB.passw,
        host=st.secrets.USER_DB.host,
        port=st.secrets.USER_DB.port,
        dbname=st.secrets.USER_DB.dbname
    )