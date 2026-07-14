from sqlalchemy import Integer, BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.common.infrastructure.db.base import Base

class ItemTemplateModel(Base):
    __tablename__ = "item_template"
    entry:Mapped[int] = mapped_column(Integer, primary_key=True) 
    name:Mapped[str] = mapped_column(String(255), nullable=False)
    display_id:Mapped[int] = mapped_column("displayid", Integer, nullable=False)
    character_class:Mapped[int] = mapped_column("class", Integer, nullable=False)