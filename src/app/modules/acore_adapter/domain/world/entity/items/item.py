from dataclasses import dataclass
from app.modules.acore_adapter.domain.acore_characters.entity.character_inventory import CharacterInventoryItem, CharacterInventoryItems
"""for compatiblity with old classes"""

@dataclass
class ItemTemplateLocale:
    id:int
    locale:str
    name:str
    description:str | None = None
    
    
@dataclass
class ItemTemplate:
    entry:int
    character_class:int
    #character_subclass:int
    name:int
    display_id:int
    # quality:int
    # inventory_type:int
    # buy_count:int = 1
    # buy_price:int=1
    # sell_price:int=1
    # allowable_class:int = -1
    # allowable_race:int = -1
    # item_level:int
    # required_level:int = 0
    # required_skill:int = 0
    # required_skill_rank:int = 0
    # max_count:int = 0
    # stackable:int = 1
    # stat_type1:int = 0
    # stat_value:int = 0
    # stat_type2:int = 0
    # stat_value2:int = 0
    # stat_type3:int = 0
    # stat_value3:int = 0
    # stat_type4:int = 0
    # stat_value4:int = 0
    # stat_type5:int = 0
    # stat_value5:int = 0
    # stat_type6:int = 0
    # stat_value6:int = 0
    # stat_type7:int = 0
    # stat_value7:int = 0 
    # stat_type8:int = 0
    # stat_value8:int = 0
    # stat_type9:int = 0
    # stat_value9:int = 0
    # stat_type10:int = 0
    # stat_value10:int = 0
    