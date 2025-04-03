from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker
import pandas as pd
import streamlit as st

# Pegando URL segura do arquivo .streamlit/secrets.toml
postgres_url = st.secrets["postgres_url"]

# Criando o motor de conexão com o banco
engine = create_engine(postgres_url)

# Base para o ORM
Base = declarative_base()

# Modelo da tabela
class ItemMudanca(Base):
    __tablename__ = 'itens_mudanca'

    id = Column(Integer, primary_key=True, autoincrement=True)
    objeto = Column(String)
    quantidade = Column(Integer)
    descricao = Column(String, nullable=True)
    valor = Column(Float, nullable=True)

# Cria a tabela no banco (se não existir)
Base.metadata.create_all(engine)