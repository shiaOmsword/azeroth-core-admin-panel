from app.modules.acore_adapter.application.acore_characters.characters.use_cases.get_character_inventory import GetCharacterInventoryItemsUseCase
from app.modules.acore_adapter.application.world.items.use_cases.get_item_template import GetItemTemplateUseCase

class GetItemNameOrchestrator:
    def __init__(
        self,
        character_inventory_use_case:GetCharacterInventoryItemsUseCase,
        item_template_use_case:GetItemTemplateUseCase,
    ):
        self.character_inventory = character_inventory_use_case
        self.item_template = item_template_use_case
        
    async def execute(self,character_id:int):
        character_items = await self.character_inventory.execute(character_id=character_id)
        item_names = [await self.item_template.execute(item.item_template_id) for item in character_items]
        return item_names