
from app.common.protocols.uows import UowsProtocol
from app.modules.acore_adapter.domain.acore_characters.entity.item_instance import ItemInstance

class UpdateInventoryItemUseCase:
    def __init__(self, uow_factory: UowsProtocol):
        self.uow_factory = uow_factory
    
    async def execute(self, item_instance_id:int) -> ItemInstance:
        async with self.uow_factory.characters_uow() as uow:
            item = await uow.item_instance.get(item_instance_id)
            #items = await uow.item_instance.update_inventory_item(character_guid=character_id)
            return item