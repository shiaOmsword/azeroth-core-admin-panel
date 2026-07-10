from app.common.protocols.uows import UowsProtocol
from app.modules.acore_adapter.infrastructure.auth.realmlist.db.dto import RealmListsDTO
import logging
logger = logging.getLogger(__name__)

class ListRealmlistsUseCase:
    def __init__(
        self,
        uows:UowsProtocol
    ):
        self.uows = uows
        
    async def execute(self, page:int, limit:int = 50) -> RealmListsDTO:
        async with self.uows.realmlists_uow() as uow:
            realms = await uow.realmlists.list(offset=page*limit)
        return realms