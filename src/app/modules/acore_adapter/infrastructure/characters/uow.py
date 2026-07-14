
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.modules.acore_adapter.infrastructure.characters.db.repositories.repository import CharacterRepository
from app.modules.acore_adapter.infrastructure.characters.db.repositories.item_inventory_repository import ItemInventoryRepository
from app.common.infrastructure.db.providers import CharactersSessionProvider
from app.common.errors.base_exceptions import UowActivationError

class CharactersUnitOfWork:
    def __init__(self, characters_provider: CharactersSessionProvider):
        self.characters_provider = characters_provider
        self.session: AsyncSession | None = None


    async def commit(self) -> None:
        if self.session is None:
            raise UowActivationError()
        await self.session.commit()
    
    async def rollback(self) -> None:
        if self.session is None:
            raise UowActivationError()
        await self.session.rollback()
        
    async def __aenter__(self):
        self.session = self.characters_provider()
        self.characters = CharacterRepository(self.session)
        self.character_inventory = ItemInventoryRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.session is None:
            return

        try:
            if exc_type:
                await self.session.rollback()
        finally:
            await self.session.close()