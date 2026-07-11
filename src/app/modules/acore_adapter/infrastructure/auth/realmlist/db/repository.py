from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.acore_adapter.infrastructure.auth.realmlist.db.models import RealmlistModel
from app.modules.acore_adapter.infrastructure.auth.realmlist.db.dto import RealmListDTO, RealmListsDTO
from app.modules.acore_adapter.infrastructure.auth.realmlist.db.mapper import RealmlistMapper

from app.common.errors.base_exceptions import NotFoundError
class RealmListNotFoundError(NotFoundError):
    pass

class RealmlistRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list(self, limit: int = 50, offset: int = 0) -> RealmListsDTO:
        stmt = (
            select(RealmlistModel)
            .limit(limit)
            .offset(offset)
            .order_by(RealmlistModel.id)
        )
        
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        realms = [RealmlistMapper.map_to_dto(model) for model in models]
        return RealmListsDTO.from_realms(realms)


    async def get_by_id(self, id:int) -> RealmlistModel | None:
        stmt = select(RealmlistModel).where(RealmlistModel.id == id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def set_local_addres(self, id: int, addres: str) -> RealmListDTO:
        realm = await self.get_by_id(id)
        if realm is None:
            raise RealmListNotFoundError()
        realm.localAddress = addres
        await self.session.flush()
        await self.session.refresh(realm)
        return RealmlistMapper.map_to_dto(realm)