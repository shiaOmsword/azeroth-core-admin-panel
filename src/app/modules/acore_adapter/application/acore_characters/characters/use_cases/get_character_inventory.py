
from app.common.protocols.uows import UowsProtocol
from app.modules.acore_adapter.domain.world.entity.items.item import CharacterInventoryItem

class GetCharacterInventoryItemsUseCase:
    def __init__(self, uow_factory: UowsProtocol):
        self.uow_factory = uow_factory
    
    async def execute(self, character_id:int) -> list[CharacterInventoryItem]:
        async with self.uow_factory.characters_uow() as uow:
            items = await uow.character_inventory.get_character_inventory_items(character_guid=character_id)
            return items