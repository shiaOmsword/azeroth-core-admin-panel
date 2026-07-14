from typing import Protocol
from sqlalchemy import select
from app.modules.acore_adapter.infrastructure.world.items.db.models.item_template_model import ItemTemplateModel
from app.modules.acore_adapter.domain.world.entity.items.item import ItemTemplate
from app.modules.acore_adapter.infrastructure.world.items.db.mapper import ItemTemplateMapper
from sqlalchemy.ext.asyncio import AsyncSession


class ItemTemplateRepositoryProtocol(Protocol):
    async def get_item_template(self, item_id:int) -> ItemTemplateModel | None:
        ...
        
        
class ItemTemplateRepository:
    def __init__(self, session:AsyncSession) -> None:
        self.session = session
        
    async def get_item_template(self, item_id:int) -> ItemTemplateModel | None:
        stmt = (
            select(ItemTemplateModel)
            .where(ItemTemplateModel.entry == item_id)
        )
        execute = await self.session.execute(stmt)
        result = execute.scalars().one_or_none()
        return ItemTemplateMapper.map_to_dto(result)
    
        
        