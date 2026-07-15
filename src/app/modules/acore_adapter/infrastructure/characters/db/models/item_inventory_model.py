from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import Integer, BigInteger, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
if TYPE_CHECKING:
    from app.modules.acore_adapter.infrastructure.characters.db.models.item_instance_model import ItemInstanceModel

from app.common.infrastructure.db.base import Base

class ItemInventoryModel(Base):
    __tablename__ = "character_inventory"
    guid:Mapped[int] = mapped_column(Integer, primary_key=True) 
    bag:Mapped[int] = mapped_column(Integer, primary_key=True,)
    slot:Mapped[int] = mapped_column(Integer, primary_key=True,)
    item:Mapped[int] = mapped_column(
        ForeignKey("item_instance.guid"),
        nullable=False
    )
    
    item_instance:Mapped[ItemInstanceModel] = relationship(
        "ItemInstanceModel",
        back_populates="item_inventory"
    )