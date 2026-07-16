from app.modules.acore_adapter.common.interface.repositories import SetsReader
from app.modules.acore_adapter.application.acore_characters.characters.use_cases.get_by_id import GetCharacterByIdUseCase
from app.modules.acore_adapter.domain.acore_characters.exceptions.errors import CharacterNotFoundError
from .get_items_name import GetItemNameOrchestrator
from app.modules.acore_adapter.application.acore_characters.item_instances.use_cases.apply_item_enchantments import ApplyItemEnchantmentsUseCase
import logging

logger = logging.getLogger(__name__)
class AutoEnchantCharacterItemsByClassUseCase:
    def __init__(
        self,
        reader:SetsReader,
        get_character_by_id_use_case:GetCharacterByIdUseCase,
        get_character_items_use_case:GetItemNameOrchestrator,
        apply_item_enchantments_use_case:ApplyItemEnchantmentsUseCase,
    ):
        self.reader = reader
        self._character = get_character_by_id_use_case
        self._items = get_character_items_use_case
    
    async def execute(
        self, 
        character_class:str,
        character_id:int,
        dry_run:bool = False,
    ):
        character = await self._character.execute(character_id)
        if not character:
            raise CharacterNotFoundError()
        
        character_items = await self._items.execute(character.guid)
        enchant_ids = self.reader.get_enchant_set(character_class)
        return enchant_ids, character_items