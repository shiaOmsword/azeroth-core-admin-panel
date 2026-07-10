from typing import Protocol
from app.modules.acore_adapter.common.protocols import CharactersUnitOfWorkFactoryProtocol, RealmlistsUnitOfWorkFactoryProtocol

class UowsProtocol(Protocol):
    characters_uow: CharactersUnitOfWorkFactoryProtocol
    realmlists_uow: RealmlistsUnitOfWorkFactoryProtocol