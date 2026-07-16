from collections.abc import Sequence
from app.common.protocols.uows import UowsProtocol
from app.modules.acore_adapter.application.acore_characters.item_instances.dto.enchantments import (
    EnchantmentChange,ApplyItemEnchantmentsResult, AppliedEnchantment
)
from app.modules.acore_adapter.application.acore_characters.item_instances.ports.enchantment_catalog import (
    EnchantmentCatalog,
)
from app.modules.acore_adapter.domain.acore_characters.item_instances.enchantments import (
    EnchantmentSlot,
    ItemEnchantments,
)
from app.modules.acore_adapter.domain.acore_characters.item_instances.errors import (
    CharacterOnlineError,
    EnchantmentNotFoundError,
    ItemInstanceNotFoundError,
    ItemOwnerNotFoundError,
    NativeRandomPropertyConflictError,
    NoFreeCustomEnchantmentSlotError,
    NoFreeEnchantmentSlotError
)



class ApplyItemEnchantmentsUseCase:
    
    def __init__(
        self,
        uow_factory: UowsProtocol,
        enchantment_catalog: EnchantmentCatalog,
    ) -> None:
        self._uow_factory = uow_factory
        self._enchantment_catalog = enchantment_catalog
            
    async def execute(
        self,
        item_instance_id: int,
        changes: Sequence[EnchantmentChange],
        *,
        dry_run: bool = False,
    ) -> ApplyItemEnchantmentsResult:
        if not changes:
            raise ValueError("At least one enchantment is required")

        async with self._uow_factory.characters_uow() as uow:
            item = await uow.item_instance.get(item_instance_id)

            if item is None:
                raise ItemInstanceNotFoundError(
                    f"Item instance {item_instance_id} was not found"
                )

            owner = await uow.characters.get_by_guid(
                item.owner_guid
            )

            if owner is None:
                raise ItemOwnerNotFoundError(
                    f"Owner {item.owner_guid} was not found"
                )

            if bool(owner.online):
                raise CharacterOnlineError(
                    "Cannot modify an item while its owner is online"
                )

            enchantments = ItemEnchantments.from_string(
                item.enchantments
            )

            applied: list[AppliedEnchantment] = []

            for change in changes:
                definition = self._enchantment_catalog.get(
                    change.enchantment_id
                )

                if definition is None:
                    raise EnchantmentNotFoundError(
                        f"Unknown enchantment ID: "
                        f"{change.enchantment_id}"
                    )

                if change.slot is None:
                    selected_slot = (
                        enchantments.first_free_custom_slot()
                    )

                    if selected_slot is None:
                        raise NoFreeEnchantmentSlotError(
                            "All custom slots are occupied"
                        )
                else:
                    selected_slot = change.slot

                previous_value = enchantments.get(
                    selected_slot
                )

                if (
                    item.random_property_id != 0
                    and previous_value.enchantment_id != 0
                ):
                    raise NativeRandomPropertyConflictError(
                        f"Slot {selected_slot.name} contains "
                        f"native enchantment "
                        f"{previous_value.enchantment_id}"
                    )

                enchantments.set_custom(
                    slot=selected_slot,
                    enchantment_id=change.enchantment_id,
                    overwrite=change.overwrite,
                )

                current_value = enchantments.get(
                    selected_slot
                )

                applied.append(
                    AppliedEnchantment(
                        slot=selected_slot,
                        previous_value=previous_value,
                        current_value=current_value,
                        enchantment=definition,
                    )
                )

            serialized = enchantments.serialize()

            if not dry_run:
                await uow.item_instance.update_enchantments(
                    item_instance_id=item_instance_id,
                    enchantments=serialized,
                )
                await uow.commit()

            return ApplyItemEnchantmentsResult(
                item_guid=item.guid,
                applied=tuple(applied),
                serialized=serialized,
                persisted=not dry_run,
            )