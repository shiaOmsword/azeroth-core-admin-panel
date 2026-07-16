
from app.common.protocols.uows import UowsProtocol
from app.modules.acore_adapter.domain.acore_characters.entity.item_instance import ItemInstance
from app.common.errors.base_exceptions import NotFoundError
import logging
logger = logging.getLogger(__name__)
from app.common.ui.console import console
from app.modules.acore_adapter.application.acore_characters.item_instances.services.enchantments import ItemEnchantments
from app.modules.acore_adapter.application.acore_characters.item_instances.services.enchantment_catalog import EnchantmentCatalog,EnchantmentSlot
from pathlib import Path

catalog = EnchantmentCatalog(
    Path("src/app/scripts/spell_item_enchantments.json")
)

class UpdateInventoryItemUseCase:
    def __init__(self, uow_factory: UowsProtocol):
        self.uow_factory = uow_factory
    
    async def execute(self, item_instance_id: int) -> ItemInstance | None:
        async with self.uow_factory.characters_uow() as uow:
            item = await uow.item_instance.get(item_instance_id)

            if item is None:
                logger.error(NotFoundError.message)
                return None
            return item
            parsed = ItemEnchantments.from_string(item.enchantments)
            parsed.set_custom(EnchantmentSlot.PROPERTY_1, 1605)
            parsed.set_custom(EnchantmentSlot.PROPERTY_2, 1107)
            new_string = parsed.serialize()
            
            console.print(new_string)

            item.enchantments = new_string
            
            await uow.item_instance.update_inventory_item(item)
            for slot, value in parsed.active():
                details = catalog.get(value.enchantment_id)
                
                if details is None:
                    console.print(
                        f"{slot.name}: unknown enchantment "
                        f"{value.enchantment_id}"
                    )
                    continue
                
                console.print(
                    f"ENCHANT_SLOT: {slot.name}\n",
                    f"ENCHANT_NAME: {details['name']}\n",
                    f"ID:{value.enchantment_id}\n",
                    f"DETAILS:{details['effect_summary']}\n",
                )
            await uow.commit()
        return item