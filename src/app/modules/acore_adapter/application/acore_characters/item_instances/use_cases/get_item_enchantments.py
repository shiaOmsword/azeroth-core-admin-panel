from app.common.protocols.uows import UowsProtocol
from app.modules.acore_adapter.application.acore_characters.item_instances.dto.enchantments import (
    ItemEnchantmentInfo,
    ItemEnchantmentsResult,
)
from app.modules.acore_adapter.application.acore_characters.item_instances.ports.enchantment_catalog import (
    EnchantmentCatalog,
)
from app.modules.acore_adapter.domain.acore_characters.item_instances.enchantments import (
    ItemEnchantments,
)
from app.modules.acore_adapter.domain.acore_characters.item_instances.errors import (
    ItemInstanceNotFoundError,
)


class GetItemEnchantmentsUseCase:
    def __init__(
        self,
        uow_factory: UowsProtocol,
        enchantment_catalog: EnchantmentCatalog,
    ) -> None:
        self._uow_factory = uow_factory
        self._enchantment_catalog = enchantment_catalog

    async def execute(self, item_instance_id: int) -> ItemEnchantmentsResult:
        async with self._uow_factory.characters_uow() as uow:
            item = await uow.item_instance.get(item_instance_id)
            if item is None:
                raise ItemInstanceNotFoundError(
                    f"Item instance {item_instance_id} was not found"
                )

            parsed = ItemEnchantments.from_string(item.enchantments)
            result: list[ItemEnchantmentInfo] = []

            for slot, value in parsed.active():
                definition = self._enchantment_catalog.get(value.enchantment_id)
                result.append(
                    ItemEnchantmentInfo(
                        slot=slot,
                        enchantment_id=value.enchantment_id,
                        duration=value.duration,
                        charges=value.charges,
                        name=definition.name if definition else None,
                        effect_summary=(
                            definition.effect_summary if definition else None
                        ),
                    )
                )

            return ItemEnchantmentsResult(
                item_guid=item.guid,
                item_entry=item.item_entry,
                enchantments=tuple(result),
            )
