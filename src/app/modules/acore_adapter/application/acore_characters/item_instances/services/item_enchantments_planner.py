from collections.abc import Sequence

from app.modules.acore_adapter.application.acore_characters.item_instances.dto.enchantments import (
    AppliedEnchantment,
    AutoEnchantItemPlan,
)
from app.modules.acore_adapter.domain.acore_characters.entity.character_inventory import (
    EnchantableEquipmentItem,
)
from app.modules.acore_adapter.domain.acore_characters.item_instances.enchantments import (
    EnchantmentDefinition,
    EnchantmentSlot,
    EnchantmentValue,
    ItemEnchantments,
)


class ItemEnchantmentsPlanner:
    """Calculate item enchantment changes without database access."""

    def plan(
        self,
        item: EnchantableEquipmentItem,
        enchantments_to_apply: Sequence[EnchantmentDefinition],
        *,
        overwrite: bool = False,
    ) -> AutoEnchantItemPlan:
        current = ItemEnchantments.from_string(item.enchantments)
        requested = tuple(enchantments_to_apply)

        if overwrite:
            applied, cleared_slots, skipped_ids = self._replace_custom_slots(
                current=current,
                requested=requested,
            )
        else:
            applied, skipped_ids = self._fill_free_slots(
                current=current,
                requested=requested,
            )
            cleared_slots = ()

        return AutoEnchantItemPlan(
            item_instance_id=item.item_instance_id,
            item_template_id=item.item_template_id,
            equipment_slot=item.equipment_slot,
            old_enchantments=item.enchantments,
            new_enchantments=current.serialize(),
            applied=applied,
            cleared_slots=cleared_slots,
            skipped_enchantment_ids=skipped_ids,
        )

    def _fill_free_slots(
        self,
        current: ItemEnchantments,
        requested: tuple[EnchantmentDefinition, ...],
    ) -> tuple[tuple[AppliedEnchantment, ...], tuple[int, ...]]:
        applied: list[AppliedEnchantment] = []
        skipped_ids: list[int] = []

        for index, definition in enumerate(requested):
            selected_slot = current.first_free_custom_slot()
            if selected_slot is None:
                skipped_ids.extend(
                    remaining.enchantment_id
                    for remaining in requested[index:]
                )
                break

            applied.append(
                self._set_enchantment(
                    current=current,
                    slot=selected_slot,
                    definition=definition,
                    overwrite=False,
                )
            )

        return tuple(applied), tuple(skipped_ids)

    def _replace_custom_slots(
        self,
        current: ItemEnchantments,
        requested: tuple[EnchantmentDefinition, ...],
    ) -> tuple[
        tuple[AppliedEnchantment, ...],
        tuple[EnchantmentSlot, ...],
        tuple[int, ...],
    ]:
        applied: list[AppliedEnchantment] = []
        cleared_slots: list[EnchantmentSlot] = []
        custom_slots = ItemEnchantments.CUSTOM_SLOTS

        for slot, definition in zip(custom_slots, requested):
            applied.append(
                self._set_enchantment(
                    current=current,
                    slot=slot,
                    definition=definition,
                    overwrite=True,
                )
            )

        first_unused_slot_index = min(len(requested), len(custom_slots))
        for slot in custom_slots[first_unused_slot_index:]:
            if current.get(slot) != EnchantmentValue():
                cleared_slots.append(slot)
            current.clear_custom(slot)

        skipped_ids = tuple(
            definition.enchantment_id
            for definition in requested[len(custom_slots):]
        )

        return tuple(applied), tuple(cleared_slots), skipped_ids

    def _set_enchantment(
        self,
        current: ItemEnchantments,
        slot: EnchantmentSlot,
        definition: EnchantmentDefinition,
        *,
        overwrite: bool,
    ) -> AppliedEnchantment:
        previous_value = current.get(slot)
        current.set_custom(
            slot=slot,
            enchantment_id=definition.enchantment_id,
            overwrite=overwrite,
        )

        return AppliedEnchantment(
            slot=slot,
            previous_value=previous_value,
            current_value=current.get(slot),
            enchantment=definition,
        )
