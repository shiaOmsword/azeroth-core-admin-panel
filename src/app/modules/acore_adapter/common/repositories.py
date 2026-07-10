from typing import Protocol
from app.modules.acore_adapter.infrastructure.characters.db.dto import CharacterDTO, CharactersDTO
from app.modules.acore_adapter.infrastructure.auth.realmlist.db.dto import RealmListDTO, RealmListsDTO


class CharactersRepositoryProtocol(Protocol):
    async def list(self, limit: int = 50, offset: int = 0) -> CharactersDTO:
        ...
    async def get_by_guid(self, guid: int) -> CharacterDTO:
        ...
        
    async def get_by_account_id(self, account_id:int) -> CharactersDTO:
        ...        
    
    async def get_by_name(self, name: str) -> CharacterDTO | None:
        ...    
        
    async def set_extra_talent(self, guid:int, value:int) -> CharacterDTO:        
        ...
        
class RealmlistRepositoryProtocol(Protocol):
    async def list(self, limit: int = 50, offset: int = 0) -> RealmListsDTO:
        ...

    async def set_local_addres(self, id: int, addres: str) -> RealmListDTO:
        ...