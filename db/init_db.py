from db.database import engine
from db.models import Base

def criar_tabelas():
    try:
        print("⏳ Criando as tabelas no banco de dados...")
        Base.metadata.create_all(bind=engine)
        print("✅ Tabelas criadas com sucesso!")
        print("ℹ️ Se as tabelas já existirem, nada será alterado.")
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")

if __name__ == "__main__":
    criar_tabelas()