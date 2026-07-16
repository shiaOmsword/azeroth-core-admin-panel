from typing import Protocol
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.modules.acore_adapter.infrastructure.characters.db.models.item_inventory_model import ItemInventoryModel
from app.modules.acore_adapter.infrastructure.characters.db.models.item_instance_model import ItemInstanceModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.acore_adapter.infrastructure.world.items.db.mapper import CharacterInventoryMapper
from app.modules.acore_adapter.domain.world.entity.items.item import CharacterInventoryItems,CharacterInventoryItem
from app.modules.acore_adapter.domain.acore_characters.entity.character_inventory import EnchantableEquipmentItem


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
    
    
    async def get_equipped_items_for_enchanting(
            self,
            character_guid: int,
        ) -> list[EnchantableEquipmentItem]:
            stmt = (
                select(
                    ItemInstanceModel.guid,
                    ItemInstanceModel.item_entry,
                    ItemInventoryModel.bag,
                    ItemInventoryModel.slot,
                    ItemInstanceModel.enchantments,
                    ItemInstanceModel.random_property_id,
                )
                .join(
                    ItemInstanceModel,
                    ItemInventoryModel.item == ItemInstanceModel.guid,
                )
                .where(
                    ItemInventoryModel.guid == character_guid,
                    ItemInventoryModel.bag == 0,
                )
                .order_by(ItemInventoryModel.slot)
            )

            result = await self.session.execute(stmt)

            return [
                EnchantableEquipmentItem(
                    item_instance_id=row.guid,
                    item_template_id=row.item_entry,
                    bag=row.bag,
                    equipment_slot=row.slot,
                    enchantments=row.enchantments,
                    random_property_id=row.random_property_id,
                )
                for row in result.all()
            ]    