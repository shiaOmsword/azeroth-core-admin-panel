from __future__ import annotations
from app.modules.acore_adapter.infrastructure.characters.db.models import CharacterModel
from app.modules.acore_adapter.infrastructure.characters.db.dto import CharacterDTO

empty_character = CharacterDTO(
    guid=0,
    name="undefined",
    level=0,
    money=0,
    account=0,
)
class CharacterMapper:
    @staticmethod
    def map_to_dto(data:CharacterModel|None) -> CharacterDTO:
        if data:
            return CharacterDTO (
                guid=data.guid,
                name=data.name,
                level=data.level,
                money=data.money,
                account=data.account,
            )
        return empty_character
        
    