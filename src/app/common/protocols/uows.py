from typing import Protocol
from app.modules.acore_adapter.common.interface.protocols import CharactersUnitOfWorkFactoryProtocol, AuthUnitOfWorkFactoryProtocol

class UowsProtocol(Protocol):
    characters_uow: CharactersUnitOfWorkFactoryProtocol
    auth_uow: AuthUnitOfWorkFactoryProtocol