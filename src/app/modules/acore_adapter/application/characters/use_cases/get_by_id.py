from app.common.protocols.uows import UowsProtocol
from app.modules.acore_adapter.infrastructure.characters.db.dto import CharacterDTO
class GetCharacterByIdUseCase:
    def __init__(
        self,
        uows:UowsProtocol
    ):
        self.uows = uows
        
    async def execute(self, gid:int) -> CharacterDTO | None:
        async with self.uows.characters_uow() as uow:
            character = await uow.characters.get_by_guid(gid) or {}
            if not character:
                return None
        return character