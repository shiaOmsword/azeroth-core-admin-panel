
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.acore_adapter.infrastructure.world.items.db.repositories.item_template_repository import ItemTemplateRepository
from app.common.infrastructure.db.providers import WorldSessionProvider
from app.common.errors.base_exceptions import UowActivationError

class WorldUnitOfWork:
    def __init__(self, world_provider: WorldSessionProvider):
        self.world_provider = world_provider
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
        self.session = self.world_provider()

        self.item_template = ItemTemplateRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.session is None:
            return

        try:
            if exc_type:
                await self.session.rollback()
        finally:
            await self.session.close()