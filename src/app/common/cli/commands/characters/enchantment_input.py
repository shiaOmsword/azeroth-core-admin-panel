from collections.abc import Sequence

from app.modules.acore_adapter.application.acore_characters.item_instances.dto.enchantments import (
    EnchantmentChange,
)
from app.modules.acore_adapter.domain.acore_characters.item_instances.enchantments import (
    EnchantmentSlot,
    ItemEnchantments,
)


class EnchantmentSetParseError(ValueError):
    """Raised when a CLI --set value cannot be converted into a change."""


def build_enchantment_changes(
    enchantment_ids: Sequence[int] = (),
    set_values: Sequence[str] = (),
    *,
    overwrite: bool = False,
) -> tuple[EnchantmentChange, ...]:
    """Build batch changes from automatic IDs and explicit SLOT:ID values.

    Explicit slots are placed first so automatic enchantments cannot consume a
    slot reserved by a --set option.
    """

    changes: list[EnchantmentChange] = []
    explicit_slots: set[EnchantmentSlot] = set()

    for raw_value in set_values:
        slot, enchantment_id = _parse_set_value(raw_value)

        if slot in explicit_slots:
            raise EnchantmentSetParseError(
                f"Slot {slot.value} is specified more than once in --set options"
            )

        explicit_slots.add(slot)
        changes.append(
            EnchantmentChange(
                enchantment_id=enchantment_id,
                slot=slot,
                overwrite=overwrite,
            )
        )

    for enchantment_id in enchantment_ids:
        if enchantment_id <= 0:
            raise EnchantmentSetParseError(
                f"Enchantment ID must be positive, got {enchantment_id}"
            )

        changes.append(
            EnchantmentChange(enchantment_id=enchantment_id)
        )

    return tuple(changes)


def _parse_set_value(raw_value: str) -> tuple[EnchantmentSlot, int]:
    value = raw_value.strip()
    slot_raw, separator, enchantment_raw = value.partition(":")

    if not separator or not slot_raw.strip() or not enchantment_raw.strip():
        raise EnchantmentSetParseError(
            f"Invalid --set value {raw_value!r}. Expected SLOT:ENCHANTMENT_ID, "
            "for example 9:1107"
        )

    try:
        slot_number = int(slot_raw.strip())
        enchantment_id = int(enchantment_raw.strip())
    except ValueError as error:
        raise EnchantmentSetParseError(
            f"Invalid --set value {raw_value!r}. Slot and enchantment ID "
            "must be integers"
        ) from error

    try:
        slot = EnchantmentSlot(slot_number)
    except ValueError as error:
        raise EnchantmentSetParseError(
            f"Unknown enchantment slot {slot_number}. Custom slots are 7 through 11"
        ) from error

    if slot not in ItemEnchantments.CUSTOM_SLOTS:
        raise EnchantmentSetParseError(
            f"Slot {slot_number} is reserved by AzerothCore. "
            "Custom slots are 7 through 11"
        )

    if enchantment_id <= 0:
        raise EnchantmentSetParseError(
            f"Enchantment ID must be positive, got {enchantment_id}"
        )

    return slot, enchantment_id
