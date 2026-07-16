from collections.abc import Sequence

from app.common.protocols.uows import UowsProtocol
from app.modules.acore_adapter.application.acore_characters.item_instances.dto.enchantments import (
    AppliedEnchantment,
    ApplyItemEnchantmentsResult,
    EnchantmentChange,
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
    DuplicateEnchantmentSlotError,
    EnchantmentNotFoundError,
    ItemInstanceNotFoundError,
    ItemOwnerNotFoundError,
    NativeRandomPropertyConflictError,
    NoFreeCustomEnchantmentSlotError,
)


class ApplyItemEnchantmentsUseCase:
    """Apply several enchantments to one item in a single transaction."""

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
        requested_changes = tuple(changes)
        if not requested_changes:
            raise ValueError("At least one enchantment is required")

        async with self._uow_factory.characters_uow() as uow:
            item = await uow.item_instance.get(item_instance_id)
            if item is None:
                raise ItemInstanceNotFoundError(
                    f"Item instance {item_instance_id} was not found"
                )

            owner = await uow.characters.get_by_guid(item.owner_guid)
            if owner is None:
                raise ItemOwnerNotFoundError(
                    f"Owner character {item.owner_guid} was not found"
                )

            if bool(owner.online):
                raise CharacterOnlineError(
                    f"Character {owner.name} is online; item modification is unsafe"
                )

            enchantments = ItemEnchantments.from_string(item.enchantments)

            # If the item has a native RandomProperty/RandomSuffix, only the custom
            # slots that were already occupied before this operation are protected.
            native_occupied_slots: set[EnchantmentSlot] = set()
            if item.random_property_id != 0:
                native_occupied_slots = {
                    slot
                    for slot in ItemEnchantments.CUSTOM_SLOTS
                    if enchantments.get(slot).enchantment_id != 0
                }

            targeted_slots: set[EnchantmentSlot] = set()
            applied: list[AppliedEnchantment] = []

            for change in requested_changes:
                definition = self._enchantment_catalog.get(change.enchantment_id)
                if definition is None:
                    raise EnchantmentNotFoundError(
                        f"Enchantment {change.enchantment_id} was not found in the catalog"
                    )

                if change.slot is None:
                    selected_slot = enchantments.first_free_custom_slot()
                    if selected_slot is None:
                        raise NoFreeCustomEnchantmentSlotError(
                            "All custom enchantment slots are occupied"
                        )
                else:
                    selected_slot = change.slot

                if selected_slot in targeted_slots:
                    raise DuplicateEnchantmentSlotError(
                        f"Slot {selected_slot.name} is targeted more than once "
                        "in the same batch"
                    )

                previous_value = enchantments.get(selected_slot)

                if selected_slot in native_occupied_slots:
                    raise NativeRandomPropertyConflictError(
                        f"Slot {selected_slot.name} contains native enchantment "
                        f"{previous_value.enchantment_id} from RandomProperty "
                        "or RandomSuffix"
                    )

                enchantments.set_custom(
                    slot=selected_slot,
                    enchantment_id=change.enchantment_id,
                    overwrite=change.overwrite,
                )
                targeted_slots.add(selected_slot)

                applied.append(
                    AppliedEnchantment(
                        slot=selected_slot,
                        previous_value=previous_value,
                        current_value=enchantments.get(selected_slot),
                        enchantment=definition,
                    )
                )

            serialized = enchantments.serialize()

            if not dry_run:
                await uow.item_instance.update_enchantments(
                    item_instance_id=item.guid,
                    enchantments=serialized,
                )
                await uow.commit()

            return ApplyItemEnchantmentsResult(
                item_guid=item.guid,
                applied=tuple(applied),
                serialized=serialized,
                persisted=not dry_run,
            )
