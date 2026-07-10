from typing import Protocol, Self
from types import TracebackType
from .repositories import CharactersRepositoryProtocol, RealmlistRepositoryProtocol



class RealmlistsUnitOfWorkProtocol(Protocol):
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
        
class RealmlistsUnitOfWorkFactoryProtocol:
    def __call__(self, *args, **kwds) -> RealmlistsUnitOfWorkProtocol:
        ...        