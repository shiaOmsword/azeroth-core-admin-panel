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
    ItemEnchantments,
)


class ItemEnchantmentsPlanner:
    """Calculate item enchantment changes without database access."""

    def plan(
        self,
        item: EnchantableEquipmentItem,
        enchantments_to_apply: Sequence[EnchantmentDefinition],
    ) -> AutoEnchantItemPlan:
        current = ItemEnchantments.from_string(item.enchantments)
        requested = tuple(enchantments_to_apply)
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

            previous_value = current.get(selected_slot)
            current.set_custom(
                slot=selected_slot,
                enchantment_id=definition.enchantment_id,
            )

            applied.append(
                AppliedEnchantment(
                    slot=selected_slot,
                    previous_value=previous_value,
                    current_value=current.get(selected_slot),
                    enchantment=definition,
                )
            )

        return AutoEnchantItemPlan(
            item_instance_id=item.item_instance_id,
            item_template_id=item.item_template_id,
            equipment_slot=item.equipment_slot,
            old_enchantments=item.enchantments,
            new_enchantments=current.serialize(),
            applied=tuple(applied),
            skipped_enchantment_ids=tuple(skipped_ids),
        )
