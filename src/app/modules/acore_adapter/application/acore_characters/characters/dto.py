from typing import Any
from dataclasses import dataclass
from app.modules.acore_adapter.domain.acore_characters.entity.character import CharacterDTO
from app.modules.acore_adapter.common.constants.gender import get_character_gender_name
from app.modules.acore_adapter.common.constants.races import get_character_race_name
from app.modules.acore_adapter.common.constants.classes import get_character_classes_name
from app.modules.acore_adapter.common.utils.format import format_money
from typing import Literal

@dataclass
class CharacterReadDTO:
    guid:int
    account:int
    name:str
    level:int
    money:int
    race:str
    character_class:int
    gender:str
    xp:int
    skin:int
    total_time:int
    zone:int
    health:int
    power1:int
    items:dict
    extraBonusTalentCount: int = 0
    online: int = 0
    
    
    @classmethod
    def map_to_read_dto(cls, data:CharacterDTO, inventory:Any | None = None):
        
        mock_items =["None"]
        if not inventory:
            items = mock_items
        else:
            items = [item for item in inventory]
        if data:
            return CharacterReadDTO (
                guid=data.guid,
                name=data.name,
                level=data.level,
                money=format_money(data.money),
                account=data.account,
                extraBonusTalentCount=data.extraBonusTalentCount,
                online=data.online,
                race=get_character_race_name(data.race),
                character_class=get_character_classes_name(data.character_class),
                gender=get_character_gender_name(data.gender),
                xp=data.xp,
                skin=data.skin,
                total_time=data.total_time,
                zone=data.zone,
                health=data.health,
                power1=data.power1,
                items=items,
            )