from sqlalchemy import Integer, BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.common.infrastructure.db.base import Base

class CharacterModel(Base):
    __tablename__ = "characters"
    
    guid: Mapped[int] = mapped_column(Integer, primary_key=True)
    account: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(12), nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    money: Mapped[int] = mapped_column(BigInteger, nullable=False)    