from typing import Protocol
from app.modules.acore_adapter.common.protocols import CharactersUnitOfWorkFactoryProtocol

class UowsProtocol(Protocol):
    characters_uow: CharactersUnitOfWorkFactoryProtocol