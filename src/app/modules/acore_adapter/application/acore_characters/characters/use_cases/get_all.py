from app.common.protocols.uows import UowsProtocol
from app.modules.acore_adapter.infrastructure.characters.db.dto import CharactersDTO
import logging
logger = logging.getLogger(__name__)

class ListCharactersUseCase:
    def __init__(
        self,
        uows:UowsProtocol
    ):
        self.uows = uows
        
    async def execute(self, page:int, limit:int = 50) -> CharactersDTO:
        async with self.uows.characters_uow() as uow:
            logger.info("[red]Getting characters[/red] part of db")
            characters = await uow.characters.list(offset=page*limit)
        return characters