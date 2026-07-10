
from app.common.protocols.uows import UowsProtocol
from app.modules.acore_adapter.infrastructure.characters.db.dto import CharacterDTO

class SetCharacterExtraTalentPointsUseCase:
    def __init__(self, uows:UowsProtocol) -> None:
        self.uows = uows
    
    async def execute(self, id:int, value:int) -> CharacterDTO:
        async with self.uows.characters_uow() as uow:
            character = await uow.characters.get_by_guid(id) or {}
            if character.online:
                raise ValueError("Player is online")
            char = await uow.characters.set_extra_talent(guid=id, value=value)
            await uow.commit()
        return char