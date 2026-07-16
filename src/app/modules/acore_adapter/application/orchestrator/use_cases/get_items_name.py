from app.modules.acore_adapter.application.acore_characters.characters.use_cases.get_character_inventory import GetCharacterInventoryItemsUseCase
from app.modules.acore_adapter.application.world.items.use_cases.get_item_template import GetItemTemplateUseCase
from app.modules.acore_adapter.application.acore_characters.characters.dto_.inventory_item import InventoryItem

class GetItemNameOrchestrator:
    def __init__(
        self,
        character_inventory_use_case:GetCharacterInventoryItemsUseCase,
        item_template_use_case:GetItemTemplateUseCase,
    ):
        self.character_inventory = character_inventory_use_case
        self.item_template = item_template_use_case
    
    def _combine_reselt(self, char_items:list, templates:list) -> list[InventoryItem]:
        instances_ids = []
        instances_slots =[]
        
        for item in char_items:
            instances_ids.append(item.item_instance_id)
            instances_slots.append(item.slot)
        
        item_names = []
        for template in templates:
            item_names.append(template.name)
            
        result = []
        for index in range(18):
            result.append(InventoryItem(
                slot=instances_slots[index],
                item_instance_id=instances_ids[index],
                name=item_names[index]
                )
        )
        return result
        
    async def execute(self,character_id:int):
        character_items = await self.character_inventory.execute(character_id=character_id)
        item_templates = [await self.item_template.execute(item.item_template_id) for item in character_items]
        
        
        return self._combine_reselt(character_items,item_templates)