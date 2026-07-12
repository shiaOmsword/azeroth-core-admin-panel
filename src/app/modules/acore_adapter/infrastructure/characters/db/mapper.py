from __future__ import annotations
from app.modules.acore_adapter.infrastructure.characters.db.models import CharacterModel
from app.modules.acore_adapter.domain.characters.entity.character import CharacterDTO

class CharacterMapper:
    @staticmethod
    def map_to_dto(data:CharacterModel) -> CharacterDTO|None:
        if data:
            return CharacterDTO (
                guid=data.guid,
                name=data.name,
                level=data.level,
                money=data.money,
                account=data.account,
                extraBonusTalentCount=data.extraBonusTalentCount,
                online=data.online,
                race=data.race,
                character_class=data.character_class,
                gender=data.gender,
                xp=data.xp,
                skin=data.skin,
                total_time=data.total_time,
                zone=data.zone,
                health=data.health,
                power1=data.power1,
            )
    
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
            race=data.race,
            character_class=data.character_class,
            gender=data.gender,
            xp=data.xp,
            skin=data.skin,
            total_time=data.total_time,
            zone=data.zone,
            health=data.health,
            power1=data.power1,            
        )    
    
    @staticmethod
    def update_orm(orm:CharacterModel, entity:CharacterDTO)-> None:
        orm.name = entity.name
        orm.level = entity.level
        orm.money = entity.money
        orm.account = entity.account
        orm.extraBonusTalentCount = entity.extraBonusTalentCount
        orm.race = entity.race
        orm.character_class = entity.character_class
        orm.gender = entity.gender
        orm.xp = entity.xp
        orm.skin = entity.skin
        orm.total_time = entity.total_time
        orm.zone = entity.zone
        orm.health = entity.health
        orm.power1 = entity.power1
    