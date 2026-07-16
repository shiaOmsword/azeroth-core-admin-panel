from typing import TypeVar, Type, Protocol, Any
from collections.abc import Callable, Awaitable
from app.modules.acore_adapter.application.acore_characters.characters.use_cases.get_by_id import GetCharacterByIdUseCase
from app.modules.acore_adapter.application.acore_characters.characters.use_cases.get_all import ListCharactersUseCase
from app.modules.acore_adapter.application.acore_characters.characters.use_cases.get_by_account_id import GetCharacterByAccountIdUseCase
from app.modules.acore_adapter.application.acore_characters.characters.use_cases.get_by_name import GetCharacterByCharacterNameUseCase
from app.modules.acore_adapter.application.acore_characters.characters.use_cases.set_extra_talent_points import SetCharacterExtraTalentPointsUseCase
from app.modules.acore_adapter.application.remote.use_cases.characters.set_level import SetCharacterLevelUseCase
from app.modules.acore_adapter.application.acore_characters.characters.use_cases.change_name import ChangeCharacterNameUseCase
from app.modules.acore_adapter.application.acore_characters.characters.use_cases.get_character_inventory import GetCharacterInventoryItemsUseCase
from app.modules.acore_adapter.application.acore_characters.item_instances.use_cases.get_item_enchantments import GetItemEnchantmentsUseCase
from app.modules.acore_adapter.application.acore_characters.item_instances.use_cases.apply_item_enchantment import ApplyItemEnchantmentUseCase

from app.modules.acore_adapter.application.orchestrator.use_cases.get_items_name import GetItemNameOrchestrator

class ExecutableUseCase(Protocol):
    async def execute(self, *args: Any, **kwargs: Any) -> Any:
        ...
    
        

CHARACTER_USE_CASES_GROUP:dict[str, type[ExecutableUseCase]] = {
    "get_by_id":GetCharacterByIdUseCase,
    "list":ListCharactersUseCase,
    "get_by_account_id":GetCharacterByAccountIdUseCase,
    "get_by_character_name":GetCharacterByCharacterNameUseCase,
    "set_extra_talent_points":SetCharacterExtraTalentPointsUseCase,
    "set_level":SetCharacterLevelUseCase,
    "change_name":ChangeCharacterNameUseCase,
    "character_inventory": GetCharacterInventoryItemsUseCase,
    "inventory_o":GetItemNameOrchestrator,
    "item_enchantments": GetItemEnchantmentsUseCase,
    "apply_item_enchantment": ApplyItemEnchantmentUseCase,
}

__all__ = [
    "GetCharacterByIdUseCase",
    "ListCharactersUseCase",
    "GetCharacterByAccountIdUseCase",
    "GetCharacterByCharacterNameUseCase",
    "SetCharacterExtraTalentPointsUseCase",
    "SetCharacterLevelUseCase",
    "CHARACTER_USE_CASES_GROUP",
]