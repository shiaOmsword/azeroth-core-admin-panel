from __future__ import annotations
from app.modules.acore_adapter.infrastructure.world.items.db.models.item_template_model import ItemTemplateModel
from app.modules.acore_adapter.domain.world.entity.items.item import ItemTemplate, CharacterInventoryItem
from app.modules.acore_adapter.infrastructure.characters.db.models.item_inventory_model import ItemInventoryModel

class CharacterInventoryMapper:
    @staticmethod
    def map_to_dto(data:ItemInventoryModel) -> CharacterInventoryItem:
        return CharacterInventoryItem (
            guid=data.guid,
            bag=data.bag,
            slot=data.slot,
            item_instance_id=data.item,
            item_template_id=data.item_instance.item_entry, #item template id
        )

class ItemTemplateMapper:
    @staticmethod
    def map_to_dto(data:ItemTemplateModel) -> ItemTemplate:
        return ItemTemplate(
            entry=data.entry,
            character_class=data.character_class,
            name=data.name,
            display_id=data.display_id
        )

