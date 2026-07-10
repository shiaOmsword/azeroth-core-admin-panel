from typing import Protocol, Self
from types import TracebackType
from .repositories import CharactersRepositoryProtocol


class CharactersUnitOfWorkProtocol(Protocol):
    characters: CharactersRepositoryProtocol

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