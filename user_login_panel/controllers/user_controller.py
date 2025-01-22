import streamlit as st
from user_login_panel.models.user_model import UserModel
from user_login_panel.views.user_view import UserViewHelper, UserViewRegisterAndLogin, UserViewSidebar 

class UserController:
    permission = None
    exception = None
    
    def __init__(self):
        self.model = UserModel()
        self.view_helper = UserViewHelper()
        self.view_register_login = UserViewRegisterAndLogin()
        self.view_sidebar = UserViewSidebar()
    
    def set_logged_in(self, logged=False):
        st.session_state.logged_in = logged

    def get_logged_in(self):
        return st.session_state.logged_in

    @classmethod
    def set_permission(cls, permission):
        cls.permission = permission
    
    @classmethod
    def get_permission(cls):
        return cls.permission
    
    @classmethod
    def set_exception(cls, exception):
        cls.exception = exception
    
    @classmethod
    def get_exception(cls):
        return cls.exception
    
    def handle_login(self):
        email, password = self.view_register_login.login_form()

        if st.button("Login"):
            if not self.model.is_valid_email(email):
                self.view_helper.show_message("Por favor, insira um e-mail válido.", "warning")
            else: 
                user = self.model.check_login(email, password)
                
                if user:                
                    self.set_logged_in(True)
                    self.view_sidebar.set_user(user.name)
                    self.set_permission(user.permission)
                    self.set_exception(user.exception)
                    self.view_helper.set_page("protected", True)
                else:    
                    self.view_helper.show_message("E-mail ou senha incorretos.", "warning")

    def handle_register(self):
        reg_data = self.view_register_login.register_form()
        reg_clicked, upd_clicked, del_clicked = self.view_register_login.display_action_buttons()

        if reg_clicked or upd_clicked or del_clicked:
            if not self.model.is_valid_email(reg_data["new_email"]):
                self.view_helper.show_message("Por favor, insira um e-mail válido.", "warning")
            elif reg_clicked and self.model.check_email(reg_data["new_email"]):
                self.view_helper.show_message("Usuário já cadastrado!", "warning")
            elif (upd_clicked or del_clicked) and not self.model.check_email(reg_data["new_email"]):
                self.view_helper.show_message("Usuário não cadastrado!", "warning")    
            elif (reg_clicked or upd_clicked) and not reg_data["new_name"]:
                self.view_helper.show_message("Por favor, insira um nome.", "warning")
            elif (reg_clicked or upd_clicked) and not reg_data["new_enterprise"]:
                self.view.show_message("Por favor, insira uma empresa.", "warning")
            elif (reg_clicked or upd_clicked) and not reg_data["new_position"]:
                self.view_helper.show_message("Por favor, insira um cargo.", "warning")
            elif (reg_clicked or upd_clicked or del_clicked) and not reg_data["autorization_code"]:        
                self.view_helper.show_message("Por favor, insira um código de autorização.", "warning")  
            elif (reg_clicked or upd_clicked or del_clicked) and not reg_data["autorization_code"] in st.secrets.AUTORIZATION.register_codes:
                self.view_helper.show_message("Por favor, insira um código de autorização válido.", "warning")
            elif (reg_clicked or upd_clicked) and not reg_data["new_password"]:        
                self.view_helper.show_message("Por favor, insira uma senha.", "warning")        
            elif (reg_clicked or upd_clicked) and reg_data["new_password"] != reg_data["confirm_password"]:
                self.view_helper.show_message("As senhas não coincidem.", "warning")
            elif reg_clicked and self.model.register_user(reg_data):
                self.view_helper.show_message("Usuário cadastrado com sucesso!", "success")
            elif upd_clicked and self.model.update_user(reg_data["new_email"], reg_data):
                self.view_helper.show_message("Usuário alterado com sucesso!", "success")
            elif del_clicked and self.model.delete_user(reg_data["new_email"]):
                self.view_helper.show_message("Usuário excluído com sucesso!", "success")

    def handle_tabs(self):
        tabs = self.view_register_login.login_page()
        
        with tabs[0]:
            self.handle_login()
        
        with tabs[1]:
            self.handle_register()
    
    def handle_main_page(self):
        st.set_page_config(page_title=st.secrets.MISCELLANEOUS.title, layout="wide")        
        
        self.view_helper.set_logo(st.secrets.MISCELLANEOUS.logo)
        self.view_helper.set_title(st.secrets.MISCELLANEOUS.title)
                    
        if "current_page" not in st.session_state:
            self.view_helper.set_page("login")

        if "logged_in" not in st.session_state:
            self.set_logged_in(False)

        if self.view_helper.get_page() == "login":
            self.handle_tabs()
        elif self.view_helper.get_page() == "protected":
            if self.get_logged_in():                
                self.view_sidebar.display()

                if self.view_sidebar.get_logout_button():
                    self.set_logged_in(False)
                    self.view_helper.set_page("login", True)
            else:
                self.view_helper.show_message("Você precisa fazer login para acessar esta página.", "warning")
                self.view_helper.set_page("login", True)
        
        return self.view_sidebar