from typing import Protocol
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.modules.acore_adapter.infrastructure.characters.db.models.item_inventory_model import ItemInventoryModel

from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.acore_adapter.infrastructure.world.items.db.mapper import CharacterInventoryMapper
from app.modules.acore_adapter.domain.world.entity.items.item import CharacterInventoryItems,CharacterInventoryItem


class ItemInventoryRepositoryProtocol(Protocol):
    async def get_character_inventory_items(self, character_guid:int) -> list[CharacterInventoryItem]:
        ...
        
class ItemInventoryRepository:
    def __init__(self, session:AsyncSession) -> None:
        self.session = session
        
    async def get_character_inventory_items(self, character_guid:int) -> list[CharacterInventoryItem]:
        stmt = (
            select(ItemInventoryModel)
            .options(
                selectinload(ItemInventoryModel.item_instance)
            )
            .where(ItemInventoryModel.guid == character_guid)
            .order_by(
                ItemInventoryModel.bag,
                ItemInventoryModel.slot,
            )            
        )
        result = await self.session.execute(stmt)
        items = result.scalars().all()
                
        return [CharacterInventoryMapper.map_to_dto(item) for item in items]