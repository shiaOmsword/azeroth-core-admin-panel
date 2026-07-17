from dataclasses import dataclass

from app.modules.acore_adapter.domain.acore_characters.item_instances.enchantments import (
    EnchantmentSlot,
    EnchantmentValue,
    EnchantmentDefinition
)

@dataclass(frozen=True, slots=True)
class EnchantmentChange:
    enchantment_id: int
    slot: EnchantmentSlot | None = None
    overwrite: bool = False
    

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


@dataclass(frozen=True, slots=True)
class AppliedEnchantment:
    slot: EnchantmentSlot
    previous_value: EnchantmentValue
    current_value: EnchantmentValue
    enchantment: EnchantmentDefinition


@dataclass(frozen=True, slots=True)
class ApplyItemEnchantmentsResult:
    item_guid: int
    applied: tuple[AppliedEnchantment, ...]
    serialized: str
    persisted: bool

@dataclass(frozen=True, slots=True)
class ItemEnchantmentsUpdate:
    item_instance_id: int
    enchantments: str


@dataclass(frozen=True, slots=True)
class AutoEnchantItemPlan:
    """Calculated enchantment changes for one equipped item."""

    item_instance_id: int
    item_template_id: int
    equipment_slot: int
    old_enchantments: str
    new_enchantments: str
    applied: tuple[AppliedEnchantment, ...]
    cleared_slots: tuple[EnchantmentSlot, ...]
    skipped_enchantment_ids: tuple[int, ...]

    @property
    def changed(self) -> bool:
        return self.old_enchantments != self.new_enchantments
