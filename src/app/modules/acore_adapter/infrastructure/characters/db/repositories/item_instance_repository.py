from typing import Protocol
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.modules.acore_adapter.infrastructure.characters.db.models.item_instance_model import ItemInstanceModel
from app.modules.acore_adapter.infrastructure.characters.db.mappers.item_instance_mapper import ItemInstanceMapper
from app.modules.acore_adapter.domain.acore_characters.entity.item_instance import ItemInstance

class ItemInstanceRepositoryProtocol(Protocol):
    async def get_item_entry_from_instance(self, inventory_item_guid:int) -> ItemInstanceModel:
        ...

    async def update_inventory_item(self,updated_entity:ItemInstance) -> None:
        ...
        
    async def get(self, instance_guid:int) -> ItemInstance:        
        ...
        
        
class ItemInstanceRepository:
    def __init__(self, session:AsyncSession) -> None:
        self.session = session    
    
    """Я думаю эта функция - легаси в ближайшем времени, название так себе."""
    async def get_item_entry_from_instance(self, inventory_item_guid:int) -> ItemInstanceModel:
        stmt = (
            select(ItemInstanceModel)
            .where(ItemInstanceModel.guid == inventory_item_guid)
        )
        result = await self.session.execute(stmt)
        instance = result.scalar_one_or_none()
        return instance
    
    
    async def get(self, instance_guid:int) -> ItemInstance:
        stmt = (
            select(ItemInstanceModel)
            .where(ItemInstanceModel.guid == instance_guid)
        )
        result = await self.session.execute(stmt)
        instance = result.scalar_one_or_none()
        return ItemInstanceMapper.map_orm_to_dto(instance)    
    
    async def update_inventory_item(self,updated_entity:ItemInstance) -> None:
        stmt = (
            select(ItemInstanceModel)
            .where(ItemInstanceModel.guid == updated_entity.guid)
        )
        result = await self.session.execute(stmt)
        instance = result.scalar_one_or_none()
        ItemInstanceMapper.update_orm(orm=instance,entity=updated_entity)
        await self.session.flush()
        
        