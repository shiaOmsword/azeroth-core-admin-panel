from app.common.protocols.uows import UowsProtocol
from app.modules.acore_adapter.domain.world.entity.items.item import ItemTemplate

class GetItemTemplateUseCase:
    def __init__(self, uow_factory:UowsProtocol):
        self.uow_factory = uow_factory
        
    async def execute(self, item_entry_id:int) -> ItemTemplate:
        async with self.uow_factory.world_uow() as uow:
            template = await uow.item_template.get_item_template(item_id=item_entry_id)
        return template