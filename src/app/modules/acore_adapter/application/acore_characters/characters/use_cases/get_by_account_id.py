from app.common.protocols.uows import UowsProtocol
from app.modules.acore_adapter.infrastructure.characters.db.dto import CharactersDTO
class GetCharacterByAccountIdUseCase:
    """Get all characters by account id"""
    def __init__(
        self,
        uows:UowsProtocol
    ):
        self.uows = uows
        
    async def execute(self, account_id:int) -> CharactersDTO:
        async with self.uows.characters_uow() as uow:
            characters = await uow.characters.get_by_account_id(account_id=account_id) or {}
        return characters