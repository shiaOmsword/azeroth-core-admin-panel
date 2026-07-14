from sqlalchemy import Integer, BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.common.infrastructure.db.base import Base

class ItemInstanceModel(Base):
    __tablename__ = "item_instance"
    guid:Mapped[int] = mapped_column(Integer, primary_key=True) 
    item_entry:Mapped[int] = mapped_column("itemEntry",Integer, nullable=False)
    owner_guid:Mapped[int] = mapped_column(Integer, primary_key=True,)
