from sqlalchemy import Integer, BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.common.infrastructure.db.base import Base

class ItemInventoryModel(Base):
    __tablename__ = "character_inventory"
    guid:Mapped[int] = mapped_column(Integer, primary_key=True) 
    bag:Mapped[int] = mapped_column(Integer, primary_key=True,)
    slot:Mapped[int] = mapped_column(Integer, primary_key=True,)
    item:Mapped[int] = mapped_column(Integer, nullable=False)