from app.modules.acore_adapter.application.acore_characters.item_instances.dto.enchantments import (
    ApplyItemEnchantmentResult,
    EnchantmentChange,
)
from app.modules.acore_adapter.application.acore_characters.item_instances.use_cases.apply_item_enchantments import (
    ApplyItemEnchantmentsUseCase,
)
from app.modules.acore_adapter.domain.acore_characters.item_instances.enchantments import (
    EnchantmentSlot,
)


class ApplyItemEnchantmentUseCase:
    """Compatibility wrapper around the batch enchantment use case."""

    def __init__(
        self,
        apply_item_enchantments_use_case: ApplyItemEnchantmentsUseCase,
    ) -> None:
        self._apply_many = apply_item_enchantments_use_case

    async def execute(
        self,
        item_instance_id: int,
        enchantment_id: int,
        slot: EnchantmentSlot | None = None,
        overwrite: bool = False,
        dry_run: bool = False,
    ) -> ApplyItemEnchantmentResult:
        result = await self._apply_many.execute(
            item_instance_id=item_instance_id,
            changes=(
                EnchantmentChange(
                    enchantment_id=enchantment_id,
                    slot=slot,
                    overwrite=overwrite,
                ),
            ),
            dry_run=dry_run,
        )

        applied = result.applied[0]
        return ApplyItemEnchantmentResult(
            item_guid=result.item_guid,
            selected_slot=applied.slot,
            enchantment_id=applied.enchantment.enchantment_id,
            enchantment_name=applied.enchantment.name,
            effect_summary=applied.enchantment.effect_summary,
            previous_value=applied.previous_value,
            current_value=applied.current_value,
            serialized=result.serialized,
            persisted=result.persisted,
        )
