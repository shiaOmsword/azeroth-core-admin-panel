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
    race: Mapped[int] = mapped_column(Integer, nullable=False)
    character_class: Mapped[int] = mapped_column("class", Integer, nullable=False, )
    gender: Mapped[int] = mapped_column(Integer, nullable=False)
    xp: Mapped[int] = mapped_column(Integer, nullable=False)
    skin: Mapped[int] = mapped_column(Integer, nullable=False)
    total_time: Mapped[int] = mapped_column("totaltime", Integer, nullable=False)
    zone: Mapped[int] = mapped_column(Integer, nullable=False)
    health: Mapped[int] = mapped_column(Integer, nullable=False)
    power1: Mapped[int] = mapped_column(Integer, nullable=False)
    extraBonusTalentCount: Mapped[int] = mapped_column(Integer, nullable=False, default=0)   
    online: Mapped[int] = mapped_column(Integer, nullable=False, default=0)   
    equipment_cache: Mapped[str] = mapped_column("equipmentCache", String, nullable=False)