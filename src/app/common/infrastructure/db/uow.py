from app.modules.acore_adapter.infrastructure.characters.db.uow import CharactersUnitOfWork
from app.common.infrastructure.db.providers import CharactersSessionProvider
from dataclasses import dataclass

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