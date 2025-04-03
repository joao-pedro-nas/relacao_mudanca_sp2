from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Para uso no Streamlit Cloud com st.secrets
from streamlit.runtime.scriptrunner import get_script_run_ctx
import streamlit as st

load_dotenv()

# Tenta pegar a URL do banco de forma segura, compatível com Streamlit Cloud
def get_postgres_url():
    # Se estiver rodando no Streamlit
    if get_script_run_ctx() is not None and "postgres_url" in st.secrets:
        return st.secrets["postgres_url"]
    # Se estiver rodando localmente
    return os.getenv("POSTGRES_URL")
# Cria a engine do banco
postgres_url = get_postgres_url()
if not postgres_url:
    raise ValueError("❌ URL do banco não encontrada. Verifique o secrets.toml ou as variáveis de ambiente.")

engine = create_engine(postgres_url, echo=False)

# Cria um criador de sessões
SessionLocal = sessionmaker(bind=engine)

# Base declarativa para os modelos (ex: Item)
Base = declarative_base()

# Função para obter sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()