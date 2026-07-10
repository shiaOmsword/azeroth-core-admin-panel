from __future__ import annotations
from dataclasses import dataclass

@dataclass
class CharacterDTO:
    guid:int
    account:int
    name:str
    level:int
    money:int
    
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