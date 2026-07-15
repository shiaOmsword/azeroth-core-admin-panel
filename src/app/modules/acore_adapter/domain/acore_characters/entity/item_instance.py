from dataclasses import dataclass

@dataclass
class ItemInstance:
    guid:int
    item_entry:int
    owner_guid:int
    count:int
    enchantments:str
    random_property_id:int
    played_time:int
    