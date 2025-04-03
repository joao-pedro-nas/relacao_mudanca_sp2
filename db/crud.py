from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from db.models import Item
import pandas as pd

# 📥 Carrega todos os itens do banco para um DataFrame
def get_all_items(db: Session) -> pd.DataFrame:
    items = db.execute(select(Item)).scalars().all()
    data = [item.as_dict() for item in items]
    return pd.DataFrame(data)

# ➕ Adiciona um novo item
def add_item(db: Session, item_data: dict):
    item = Item(**item_data)
    db.add(item)
    db.commit()

# ✏️ Atualiza um item existente com base no nome
def update_item(db: Session, nome_objeto: str, novos_dados: dict):
    db.execute(
        update(Item)
        .where(Item.objeto == nome_objeto)
        .values(**novos_dados)
    )
    db.commit()

# ❌ Remove um item com base no nome
def delete_item(db: Session, nome_objeto: str):
    db.execute(
        delete(Item).where(Item.objeto == nome_objeto)
    )
    db.commit()

# 🔁 Substitui todos os registros no banco com base em um DataFrame
def replace_all_items(db: Session, df: pd.DataFrame):
    db.execute(delete(Item))
    for _, row in df.iterrows():
        item = Item(
            objeto=row["objeto"],
            quantidade=int(row["quantidade"]),
            descricao=row["descricao"] if pd.notna(row["descricao"]) else None,
            valor=int(row["valor"]) if pd.notna(row["valor"]) else None
        )
        db.add(item)
    db.commit()