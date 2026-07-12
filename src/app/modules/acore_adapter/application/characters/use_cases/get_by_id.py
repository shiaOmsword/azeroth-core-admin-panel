from app.common.protocols.uows import UowsProtocol
from app.modules.acore_adapter.infrastructure.characters.db.dto import CharacterDTO
from app.modules.acore_adapter.application.characters.dto import CharacterReadDTO
from app.modules.acore_adapter.domain.characters.exceptions.errors import NotFoundError
import logging

logger = logging.getLogger(__name__)

class GetCharacterByIdUseCase:
    """Get one character by gid from database"""
    def __init__(
        self,
        uows:UowsProtocol
    ):
        self.uows = uows
        
    async def execute(self, gid:int) -> CharacterDTO | None:
        async with self.uows.characters_uow() as uow:
            character = await uow.characters.get_by_guid(gid) or {}
            if not character:
                logger.warning("%s",NotFoundError().message)
                return None
        return CharacterReadDTO.map_to_read_dto(character)