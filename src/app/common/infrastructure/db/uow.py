from app.modules.acore_adapter.infrastructure.characters.db.uow import CharactersUnitOfWork
from app.modules.acore_adapter.infrastructure.auth.realmlist.db.uow import RealmlistUnitOfWork

from app.common.infrastructure.db.providers import (
    CharactersSessionProvider, 
    AuthSessionProvider
)
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class RealmlistsUnitOfWorkFactory:
    auth_provider: AuthSessionProvider
    
    def __call__(self, *args, **kwds):
        return RealmlistUnitOfWork(
            auth_provider=self.auth_provider
        )    
    
@dataclass(frozen=True, slots=True)
class CharactersUnitOfWorkFactory:
    characters_provider: CharactersSessionProvider
    
    def __call__(self, *args, **kwds):
        return CharactersUnitOfWork(
            characters_provider=self.characters_provider
        )


@dataclass(frozen=True, slots=True)
class UnitsOfWork:
    characters_uow: CharactersUnitOfWorkFactory
    realmlists_uow: RealmlistsUnitOfWorkFactory