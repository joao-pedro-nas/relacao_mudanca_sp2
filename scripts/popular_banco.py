import pandas as pd
from db.database import get_db
from db.models import Item

CSV_PATH = "data/itens_pro2.csv"

# Lê o CSV original
df = pd.read_csv(CSV_PATH)

# Remove linhas inválidas (sem nome, sem quantidade etc.)
df = df.dropna(subset=["objeto", "quantidade"])

# Inicia a sessão com o banco
db_gen = get_db()  # Isso retorna um generator
db = next(db_gen)  # Pega a sessão propriamente dita

try:
    # Limpa o banco antes de popular
    db.query(Item).delete()

    # Adiciona os registros
    for _, row in df.iterrows():
        item = Item(
            objeto=row["objeto"],
            quantidade=int(row["quantidade"]),
            descricao=row["descricao"] if pd.notna(row["descricao"]) else None,
            valor=int(row["valor"]) if pd.notna(row["valor"]) else None
        )
        db.add(item)

    db.commit()
    print("✅ Banco populado com sucesso!")

finally:
    # Fecha a sessão corretamente
    db_gen.close()