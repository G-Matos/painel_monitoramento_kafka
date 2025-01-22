import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import hashlib
import re
from user_login_panel.config.database import get_db_url

Base = declarative_base()

class User(Base):
    __tablename__ = f"users_{st.secrets.MISCELLANEOUS.subject}"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    enterprise = Column(String, nullable=False)
    position = Column(String, nullable=False)
    permission = Column(String, nullable=False)
    exception = Column(String, nullable=False)
    autorization = Column(String, nullable=False)
    password = Column(String, nullable=False)

class UserModel:
    def __init__(self):
        self.engine = create_engine(get_db_url())
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def check_email(self, email):
        session = self.Session()
        
        try:
            return session.query(User).filter_by(email=email).first() is not None
        finally:
            session.close()

    def check_login(self, email, password):
        session = self.Session()
        
        try:
            hashed_password = self.hash_password(password)
            return session.query(User).filter_by(email=email, password=hashed_password).first() 
        finally:
            session.close()

    def register_user(self, inserted_data):
        session = self.Session()
        hashed_password = self.hash_password(inserted_data["new_password"])
        
        try:
            if session.query(User).filter_by(email=inserted_data["new_email"]).first():
                return False  # Usuário já cadastrado

            new_user = User(
                email=inserted_data["new_email"],
                name=inserted_data["new_name"],
                enterprise=inserted_data["new_enterprise"],
                position=inserted_data["new_position"],
                permission=inserted_data["new_permission"],
                exception=inserted_data["new_exception"],
                autorization=inserted_data["autorization_code"],
                password=hashed_password
            )
            
            session.add(new_user)
            session.commit()            
            return True  # Usuário cadastrado com sucesso
        finally:
            session.close()
    
    def update_user(self, email, updated_data):
        session = self.Session()
        
        try:
            user = session.query(User).filter_by(email=email).first()
            
            if user:
                user.name = updated_data.get("new_name", user.name)
                user.enterprise = updated_data.get("new_enterprise", user.enterprise)
                user.position = updated_data.get("new_position", user.position)
                user.permission = updated_data.get("new_permission", user.permission)
                user.exception = updated_data.get("new_exception", user.exception)
                user.autorization = updated_data.get("autorization_code", user.autorization)
                
                if "new_password" in updated_data:
                    user.password = self.hash_password(updated_data["new_password"])
                
                session.commit()                
                return True
            
            return False
        finally:
            session.close()

    def delete_user(self, email):
        session = self.Session()
        
        try:
            user = session.query(User).filter_by(email=email).first()
            
            if user:
                session.delete(user)
                session.commit()                
                return True
            
            return False
        finally:
            session.close()

    @staticmethod
    def is_valid_email(email):
        regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.match(regex, email)