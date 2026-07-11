
from app.common.protocols.uows import UowsProtocol
from app.modules.acore_adapter.infrastructure.characters.db.dto import CharacterDTO
from app.modules.acore_adapter.domain.characters.exceptions.errors import CharacterIsOnlineError
import logging
logger = logging.getLogger(__name__)
class SetCharacterExtraTalentPointsUseCase:
    def __init__(self, uows:UowsProtocol) -> None:
        self.uows = uows
    
    async def execute(self, id:int, value:int) -> CharacterDTO|None:
        async with self.uows.characters_uow() as uow:
            character = await uow.characters.get_by_guid(id) or {}
            if character.online:
                logger.error("%s",CharacterIsOnlineError().message)
                return
            char = await uow.characters.set_extra_talent(guid=id, value=value)
            await uow.commit()
        return char