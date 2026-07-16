from dataclasses import dataclass

from app.modules.acore_adapter.domain.acore_characters.item_instances.enchantments import (
    EnchantmentSlot,
    EnchantmentValue,
)


@dataclass(frozen=True, slots=True)
class ItemEnchantmentInfo:
    slot: EnchantmentSlot
    enchantment_id: int
    duration: int
    charges: int
    name: str | None
    effect_summary: str | None


@dataclass(frozen=True, slots=True)
class ItemEnchantmentsResult:
    item_guid: int
    item_entry: int
    enchantments: tuple[ItemEnchantmentInfo, ...]


@dataclass(frozen=True, slots=True)
class ApplyItemEnchantmentResult:
    item_guid: int
    selected_slot: EnchantmentSlot
    enchantment_id: int
    enchantment_name: str
    effect_summary: str
    previous_value: EnchantmentValue
    current_value: EnchantmentValue
    serialized: str
    persisted: bool
