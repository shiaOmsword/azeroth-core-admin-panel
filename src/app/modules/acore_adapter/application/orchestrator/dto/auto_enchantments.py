from dataclasses import dataclass

from app.modules.acore_adapter.application.acore_characters.item_instances.dto.enchantments import (
    AutoEnchantItemPlan,
)


@dataclass(frozen=True, slots=True)
class AutoEnchantCharacterResult:
    character_guid: int
    character_name: str
    character_class: str
    requested_enchantment_ids: tuple[int, ...]
    items: tuple[AutoEnchantItemPlan, ...]
    updated_item_count: int
    skipped_enchantment_count: int
    persisted: bool
