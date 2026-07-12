from __future__ import annotations
from app.modules.acore_adapter.infrastructure.characters.db.models import CharacterModel
from app.modules.acore_adapter.domain.characters.entity.character import CharacterDTO

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
                extraBonusTalentCount=data.extraBonusTalentCount,
                online=data.online,
            )
        return empty_character
    
    @staticmethod
    def map_to_orm(data:CharacterDTO) -> CharacterModel:
        return CharacterModel(
            guid=data.guid,
            name=data.name,
            level=data.level,
            money=data.money,
            account=data.account,
            extraBonusTalentCount=data.extraBonusTalentCount,
            online=data.online, 
        )    
    
    @staticmethod
    def update_orm(orm:CharacterModel, entity:CharacterDTO)-> None:
        orm.name = entity.name
        orm.level = entity.level
        orm.money = entity.money
        orm.account = entity.account
        orm.extraBonusTalentCount = entity.extraBonusTalentCount
    