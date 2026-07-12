
from app.common.protocols.uows import UowsProtocol
from app.modules.acore_adapter.infrastructure.characters.db.dto import CharacterDTO
from app.modules.acore_adapter.domain.characters.exceptions.errors import CharacterIsOnlineError
import logging
logger = logging.getLogger(__name__)

class ChangeCharacterNameUseCase:
    def __init__(self, uows:UowsProtocol) -> None:
        self.uows = uows
    
    async def execute(self, char_id:int, value:str) -> CharacterDTO|None:
        async with self.uows.characters_uow() as uow:
            character = await uow.characters.get_by_guid(char_id) or {}
            if character.online:
                logger.error("%s",CharacterIsOnlineError().message)
                return
            #Здесь проверка имени и валидация
            
            character.name = value.strip()
            await uow.characters.update(character)
            await uow.commit()
        return character