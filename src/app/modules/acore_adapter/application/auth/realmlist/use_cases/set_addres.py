from app.common.protocols.uows import UowsProtocol
from app.modules.acore_adapter.infrastructure.auth.realmlist.db.dto import RealmListDTO
import logging
logger = logging.getLogger(__name__)

class SetRealmlistAddresUseCase:
    def __init__(
        self,
        uows:UowsProtocol
    ):
        self.uows = uows
        
    async def execute(self, id:int, addres:str) -> RealmListDTO:
        async with self.uows.realmlists_uow() as uow:
            realm = await uow.realmlists.set_local_addres(id=id,addres=addres)
            await uow.commit()
        return realm