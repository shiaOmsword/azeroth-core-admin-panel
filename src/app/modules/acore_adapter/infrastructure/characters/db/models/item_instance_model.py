from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import Integer, BigInteger, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.common.infrastructure.db.base import Base

if TYPE_CHECKING:
    from app.modules.acore_adapter.infrastructure.characters.db.models.item_inventory_model import ItemInventoryModel


class ItemInstanceModel(Base):
    __tablename__ = "item_instance"
    guid:Mapped[int] = mapped_column(Integer, primary_key=True) 
    item_entry:Mapped[int] = mapped_column("itemEntry",Integer, nullable=False)
    owner_guid:Mapped[int] = mapped_column(Integer, nullable=False)
    count:Mapped[int] = mapped_column(Integer, nullable=False)
    enchantments:Mapped[str] = mapped_column(Text, nullable=False)
    random_property_id:Mapped[int] = mapped_column("randomPropertyId",Integer, nullable=False)
    played_time:Mapped[int]=mapped_column("playedTime", Integer, nullable=False)
    item_inventory:Mapped[ItemInventoryModel] = relationship(
        "ItemInventoryModel",
        back_populates="item_instance",
        uselist=False,
    )