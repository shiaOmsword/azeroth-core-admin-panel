from app.common.protocols.uows import UowsProtocol
from app.modules.acore_adapter.infrastructure.characters.db.dto import CharacterDTO
from app.modules.acore_adapter.application.acore_characters.characters.dto import CharacterReadDTO
import logging
logger = logging.getLogger(__name__)
from app.modules.acore_adapter.domain.acore_characters.exceptions.errors import NotFoundError

from app.modules.acore_adapter.application.orchestrator.use_cases.get_items_name import GetItemNameOrchestrator
class GetCharacterByCharacterNameUseCase:
    """Get one character by name from database"""
    def __init__(
        self,
        uows:UowsProtocol,
        item_names_use_case:GetItemNameOrchestrator
    ):
        self.uows = uows
        self.item_names = item_names_use_case
        
    async def execute(self, name:str) -> CharacterDTO | None:
        async with self.uows.characters_uow() as uow:
            character = await uow.characters.get_by_name(name=name) or {}
        
            if not character:
                logger.warning("%s",NotFoundError().message)
                return None
        character_item_names = await self.item_names.execute(character_id=character.guid)
        return CharacterReadDTO.map_to_read_dto(character, character_item_names)