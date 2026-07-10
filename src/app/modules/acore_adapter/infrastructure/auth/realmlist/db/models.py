
    
from sqlalchemy import Integer, BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.common.infrastructure.db.base import Base

class RealmlistModel(Base):
    __tablename__ = "realmlist"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(32), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    localAddress: Mapped[str] = mapped_column(String(255), nullable=False)        