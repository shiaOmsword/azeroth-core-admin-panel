from typing import Protocol, Self
from types import TracebackType

from .repositories import CharactersRepositoryProtocol, RealmlistRepositoryProtocol
from app.modules.acore_adapter.infrastructure.characters.db.repositories.item_inventory_repository import ItemInventoryRepositoryProtocol
from app.modules.acore_adapter.infrastructure.world.items.db.repositories.item_template_repository import ItemTemplateRepositoryProtocol

class WorldUnitOfWorkProtocol(Protocol):
    item_template: ItemTemplateRepositoryProtocol
    async def commit(self) -> None:
        ...
        
    async def rollback(self) -> None:
        ...

    async def __aenter__(self) -> Self:
        ...

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        ...   
        
class AuthUnitOfWorkProtocol(Protocol):
    realmlists: RealmlistRepositoryProtocol
    async def commit(self) -> None:
        ...
        
    async def rollback(self) -> None:
        ...

    async def __aenter__(self) -> Self:
        ...

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        ...   
    
class CharactersUnitOfWorkProtocol(Protocol):
    characters: CharactersRepositoryProtocol
    character_inventory:ItemInventoryRepositoryProtocol

    async def commit(self) -> None:
        ...
        
    async def rollback(self) -> None:
        ...

    async def __aenter__(self) -> Self:
        ...

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        ...
        
class CharactersUnitOfWorkFactoryProtocol:
    def __call__(self, *args, **kwds) -> CharactersUnitOfWorkProtocol:
        ...
        
class AuthUnitOfWorkFactoryProtocol:
    def __call__(self, *args, **kwds) -> AuthUnitOfWorkProtocol:
        ...
        
class WorldUnitOfWorkFactoryProtocol:
    def __call__(self, *args, **kwds) -> WorldUnitOfWorkProtocol:
        ...  