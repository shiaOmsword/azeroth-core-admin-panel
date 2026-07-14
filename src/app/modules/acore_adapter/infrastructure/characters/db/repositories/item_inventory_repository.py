from typing import Protocol
from sqlalchemy import select
from app.modules.acore_adapter.infrastructure.characters.db.models.item_inventory_model import ItemInventoryModel
from app.modules.acore_adapter.infrastructure.characters.db.models.item_instance_model import ItemInstanceModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.acore_adapter.infrastructure.world.items.db.mapper import CharacterInventoryMapper
from app.modules.acore_adapter.domain.world.entity.items.item import CharacterInventoryItems,CharacterInventoryItem


class ItemInventoryRepositoryProtocol(Protocol):
    async def get_character_inventory_items(self, character_guid:int) -> list[CharacterInventoryItem]:
        ...
        
        
class ItemInventoryRepository:
    def __init__(self, session:AsyncSession) -> None:
        self.session = session
        
    async def get_item_entry_from_instance(self, inventory_item_guid:int) -> ItemInstanceModel:
        stmt = (
            select(ItemInstanceModel)
            .where(ItemInstanceModel.guid == inventory_item_guid)
        )
        result = await self.session.execute(stmt)
        instance = result.scalar_one_or_none()
        return instance
        
    async def get_character_inventory_items(self, character_guid:int) -> list[CharacterInventoryItem]:
        stmt = (
            select(ItemInventoryModel)
            .where(ItemInventoryModel.guid == character_guid)
            .order_by(
                ItemInventoryModel.bag,
                ItemInventoryModel.slot,
            )            
        )
        result = await self.session.execute(stmt)
        items = result.scalars().all()
        
        item_templates = [await self.get_item_entry_from_instance(item.item) for item in items]
        
        def build_result(items=items, item_templates=item_templates):
            dtos = []
            for index, item in enumerate(items):
                dtos.append(CharacterInventoryMapper.map_to_dto(item, item_templates[index]))
            return dtos
                
        return build_result()