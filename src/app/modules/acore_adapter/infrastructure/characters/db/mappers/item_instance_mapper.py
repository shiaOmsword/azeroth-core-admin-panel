from app.modules.acore_adapter.infrastructure.characters.db.models.item_instance_model import ItemInstanceModel
from app.modules.acore_adapter.domain.acore_characters.entity.item_instance import ItemInstance
from dataclasses import dataclass

@dataclass
class ItemInstanceMapper:
    @staticmethod
    def map_orm_to_dto(item_orm:ItemInstanceModel) -> ItemInstance:
        return ItemInstance(
            guid=item_orm.guid,
            item_entry=item_orm.item_entry,
            owner_guid=item_orm.owner_guid,
            count=item_orm.count,
            enchantments=item_orm.enchantments,
            random_property_id=item_orm.random_property_id,
            played_time=item_orm.played_time,
        )
    
    @staticmethod
    def update_orm(orm:ItemInstanceModel, entity:ItemInstance) -> None:
            orm.guid=entity.guid,
            orm.item_entry=entity.item_entry,
            orm.owner_guid=entity.owner_guid,
            orm.count=entity.count,
            orm.enchantments=entity.enchantments,
            orm.random_property_id=entity.random_property_id,
            orm.played_time=entity.played_time