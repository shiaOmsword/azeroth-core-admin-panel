from app.common.protocols.uows import UowsProtocol
from app.modules.acore_adapter.application.acore_characters.item_instances.dto.enchantments import (
    ApplyItemEnchantmentResult,
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
)


class ApplyItemEnchantmentUseCase:
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
        enchantment_id: int,
        slot: EnchantmentSlot | None = None,
        overwrite: bool = False,
        dry_run: bool = False,
    ) -> ApplyItemEnchantmentResult:
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

            # if item.random_property_id != 0:
            #     raise NativeRandomPropertyConflictError(
            #         "The item already uses RandomProperty or RandomSuffix"
            #     )

            definition = self._enchantment_catalog.get(enchantment_id)
            if definition is None:
                raise EnchantmentNotFoundError(
                    f"Enchantment {enchantment_id} was not found in the catalog"
                )

            enchantments = ItemEnchantments.from_string(item.enchantments)

            if slot is None:
                selected_slot = enchantments.first_free_custom_slot()
                if selected_slot is None:
                    raise NoFreeCustomEnchantmentSlotError(
                        "All custom enchantment slots are occupied"
                    )
                #previous_value = enchantments.get(selected_slot)
                #enchantments.add_custom(enchantment_id)
            else:
                selected_slot = slot
                
            current_value = enchantments.get(selected_slot)    
            
            if (
                item.random_property_id != 0
                and current_value.enchantment_id != 0
            ):         
                raise NativeRandomPropertyConflictError(
                    f"Slot {selected_slot.name} is occupied by "
                    f"native RandomProperty or RandomSuffix enchantment "
                    f"{current_value.enchantment_id}"
            )       
            
            previous_value = enchantments.get(selected_slot)
            enchantments.set_custom(
                slot=selected_slot,
                enchantment_id=enchantment_id,
                overwrite=overwrite,
            )

            current_value = enchantments.get(selected_slot)
            serialized = enchantments.serialize()

            if not dry_run:
                await uow.item_instance.update_enchantments(
                    item_instance_id=item.guid,
                    enchantments=serialized,
                )
                # CharactersUnitOfWork currently does not auto-commit on success.
                await uow.commit()

            return ApplyItemEnchantmentResult(
                item_guid=item.guid,
                selected_slot=selected_slot,
                enchantment_id=enchantment_id,
                enchantment_name=definition.name,
                effect_summary=definition.effect_summary,
                previous_value=previous_value,
                current_value=current_value,
                serialized=serialized,
                persisted=not dry_run,
            )
