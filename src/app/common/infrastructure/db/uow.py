from app.modules.acore_adapter.infrastructure.characters.uow import CharactersUnitOfWork
from app.modules.acore_adapter.infrastructure.auth.auth_uow import AuthUnitOfWork
from app.modules.acore_adapter.infrastructure.world.uow import WorldUnitOfWork

from app.common.infrastructure.db.providers import (
    CharactersSessionProvider, AuthSessionProvider, WorldSessionProvider
)
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AuthUnitOfWorkFactory:
    auth_provider: AuthSessionProvider

    def __call__(self) -> AuthUnitOfWork:
        return AuthUnitOfWork(
            auth_provider=self.auth_provider,
        )
    
@dataclass(frozen=True, slots=True)
class CharactersUnitOfWorkFactory:
    characters_provider: CharactersSessionProvider
    
    def __call__(self, *args, **kwds):
        return CharactersUnitOfWork(
            characters_provider=self.characters_provider
        )
        
@dataclass(frozen=True, slots=True)
class WorldUnitOfWorkFactory:
    world_provider: WorldSessionProvider
    
    def __call__(self, *args, **kwds):
        return WorldUnitOfWork(
            world_provider=self.world_provider
        )        


@dataclass(frozen=True, slots=True)
class UnitsOfWork:
    characters_uow: CharactersUnitOfWorkFactory
    auth_uow: AuthUnitOfWorkFactory
    world_uow: WorldUnitOfWorkFactory