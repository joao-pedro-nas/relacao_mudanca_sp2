from sqlalchemy import Column, Integer, String, Float
from db.database import Base

class Item(Base):
    __tablename__ = "itens"

    id = Column(Integer, primary_key=True, index=True)
    objeto = Column(String(100), nullable=False)
    quantidade = Column(Integer, nullable=False)
    descricao = Column(String(255), nullable=True)
    valor = Column(Float, nullable=True)  # ou default=0.0, se quiser isso explícito

    def __repr__(self):
        return f"<Item(objeto='{self.objeto}', quantidade={self.quantidade}, valor={self.valor})>"
    
    def as_dict(self):
        return {
            "id": self.id,
            "objeto": self.objeto,
            "quantidade": self.quantidade,
            "descricao": self.descricao,
            "valor": self.valor
        }