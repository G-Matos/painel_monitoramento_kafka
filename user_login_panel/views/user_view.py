import streamlit as st
from datetime import datetime

class UserViewHelper:
    def __init__(self):
        # Verifica se a chave 'current_page' existe no session_state, caso contrário, cria.
        if "current_page" not in st.session_state:
            self.set_page("login")
    
    def set_logo(self, image_path):
        """
        Define o logotipo no aplicativo Streamlit.
        :param image_path: Caminho da imagem do logotipo.
        """
        st.logo(image_path)  # Corrigido para st.image (não existe st.logo)
    
    def set_title(self, title):
        """
        Define o título da página Streamlit.
        :param title: O título da página.
        """
        st.title(title)

    def show_message(self, message, level="info"):
        """
        Exibe uma mensagem no aplicativo com diferentes níveis (info, success, warning, error).
        :param message: Mensagem a ser exibida.
        :param level: Nível da mensagem (info, success, warning, error). Default é 'info'.
        """
        if level == "success":
            st.success(message)
        elif level == "warning":
            st.warning(message)
        elif level == "error":
            st.error(message)
        else:
            st.info(message)

    def set_page(self, page, refresh=False):
        """
        Define a página atual no session_state.
        :param page: O nome ou identificador da página.
        """
        st.session_state.current_page = page
        
        if refresh:
            st.rerun()  # Atualiza a página

    def get_page(self):
        return st.session_state.current_page       

class UserViewRegisterAndLogin:
    def login_page(self):
        st.subheader("Login ou Cadastro")
        return st.tabs(["Login", "Cadastrar"])

    def login_form(self):
        email = st.text_input("Email", key="login_user")
        password = st.text_input("Senha", type="password", key="login_pass")
        return email, password

    def register_form(self):
        new_email = st.text_input("Novo Email", key="register_user")
        new_name = st.text_input("Nome", key="username")
        new_enterprise = st.text_input("Empresa", key="user_enterprise")
        new_position = st.text_input("Cargo", key="user_position")
        new_permission = st.text_input("Permissão", key="user_permission")
        new_exception = st.text_input("Exceção", key="user_exception")
        autorization_code = st.text_input("Código de Autorização", type="password", key="register_code")
        new_password = st.text_input("Nova Senha", type="password", key="register_pass")
        confirm_password = st.text_input("Confirme a Senha", type="password", key="confirm_pass")

        return {
            "new_email": new_email,
            "new_name": new_name,
            "new_enterprise": new_enterprise,
            "new_position": new_position,
            "new_permission": new_permission,
            "new_exception": new_exception,
            "autorization_code": autorization_code,
            "new_password": new_password,
            "confirm_password": confirm_password
        }

    def display_action_buttons(self):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            register_button = st.button("Cadastrar", key="register_button", use_container_width=True)
        
        with col2:
            update_button = st.button("Alterar", key="update_button", use_container_width=True)
        
        with col3:
            delete_button = st.button("Excluir", key="delete_button", use_container_width=True)

        return register_button, update_button, delete_button

class UserViewSidebar:
    user = None
    
    def __init__(self):
        self.sidebar = st.sidebar
        self.search_button = None
        self.logout_button = None
        self.start_date = None
        self.end_date = None

    @classmethod
    def set_user(cls, user):
        cls.user = user
    
    @classmethod
    def get_user(cls):
        return cls.user
    
    def display(self):
        with self.sidebar:
            self.sidebar.subheader(f"Bem-vindo, {self.get_user()}!")

            col1, col2 = st.columns(2)
        
            with col1:
                self.refresh_button = st.button("Atualizar", key="refresh_button", use_container_width=True)
            
            with col2:
                self.logout_button = st.button("Logout", key="logout_button", use_container_width=True)

            self.start_date = self.sidebar.date_input(
                "Data Inicial",
                value=datetime.now(),
                min_value=datetime(2024, 1, 1),
                max_value=datetime(2050, 12, 31),
                format="DD/MM/YYYY"
            )

            self.end_date = self.sidebar.date_input(
                "Data Final",
                value=datetime.now(),
                min_value=self.start_date,
                max_value=datetime(2030, 12, 31),
                format="DD/MM/YYYY"
            )
    
    def get_sidebar(self):
        return self.sidebar
    
    def get_refresh_button(self):
        return self.refresh_button
    
    def get_logout_button(self):
        return self.logout_button
    
    def get_start_date(self):
        return self.start_date
    
    def get_end_date(self):
        return self.end_date