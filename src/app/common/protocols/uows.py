from typing import Protocol
from app.modules.acore_adapter.common.interface.protocols import CharactersUnitOfWorkFactoryProtocol, AuthUnitOfWorkFactoryProtocol, WorldUnitOfWorkFactoryProtocol

class UowsProtocol(Protocol):
    characters_uow: CharactersUnitOfWorkFactoryProtocol
    auth_uow: AuthUnitOfWorkFactoryProtocol
    world_uow: WorldUnitOfWorkFactoryProtocol