from app.common.protocols.uows import UowsProtocol
from app.modules.acore_adapter.infrastructure.characters.db.dto import CharacterDTO
from app.modules.acore_adapter.application.characters.dto import CharacterReadDTO
import logging
logger = logging.getLogger(__name__)
from app.modules.acore_adapter.domain.characters.exceptions.errors import NotFoundError
class GetCharacterByCharacterNameUseCase:
    """Get one character by name from database"""
    def __init__(
        self,
        uows:UowsProtocol
    ):
        self.uows = uows
        
    async def execute(self, name:str) -> CharacterDTO | None:
        async with self.uows.characters_uow() as uow:
            character = await uow.characters.get_by_name(name=name) or {}
            if not character:
                logger.warning("%s",NotFoundError().message)
                return None
        return CharacterReadDTO.map_to_read_dto(character)