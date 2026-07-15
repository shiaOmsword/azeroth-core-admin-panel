from __future__ import annotations
from dataclasses import dataclass

@dataclass
class CharacterDTO:
    guid:int
    account:int
    name:str
    level:int
    money:int
    race:int
    character_class:int
    gender:int
    xp:int
    skin:int
    total_time:int
    zone:int
    health:int
    power1:int
    extraBonusTalentCount: int = 0
    online: int = 0
    equipment_cache:str = ""
    
    
@dataclass
class CharactersDTO:
    characters:list[CharacterDTO]
    count:int
    
    @classmethod
    def from_characters(cls, characters:list[CharacterDTO]) -> CharactersDTO:
        return cls(
            characters=characters,
            count=len(characters)
        )