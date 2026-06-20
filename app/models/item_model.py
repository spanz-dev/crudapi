from sqlalchemy import Column, Integer, String, Float
from app.config.database import Base

class ItemModel(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False)
    preco = Column(Float, nullable=False)
    descricao = Column(String, nullable=True)