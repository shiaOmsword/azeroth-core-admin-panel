from dataclasses import dataclass
@dataclass
class CharacterInventoryItem:
    guid:int #character_id
    bag:int
    slot:int
    item_instance_id:int #item_instance_id, not template id
    item_template_id:int
    
@dataclass
class CharacterInventoryItems:
    items:list[CharacterInventoryItem]
    
@dataclass(frozen=True, slots=True)
class EnchantableEquipmentItem:
    item_instance_id: int
    item_template_id: int
    bag: int
    equipment_slot: int
    enchantments: str
    random_property_id: int        