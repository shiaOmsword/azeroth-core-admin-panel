from app.common.protocols.uows import UowsProtocol
from app.modules.acore_adapter.infrastructure.characters.db.dto import CharacterDTO
import logging
logger = logging.getLogger(__name__)
class GetCharacterByCharacterNameUseCase:
    def __init__(
        self,
        uows:UowsProtocol
    ):
        self.uows = uows
        
    async def execute(self, name:str) -> CharacterDTO | None:
        async with self.uows.characters_uow() as uow:
            character = await uow.characters.get_by_name(name=name) or {}
            if not character:
                logger.warning("Character not found")
                return None
        return character