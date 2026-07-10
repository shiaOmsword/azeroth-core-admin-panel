from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.modules.acore_adapter.infrastructure.auth.realmlist.db.repository import RealmlistRepository
from app.common.infrastructure.db.providers import AuthSessionProvider

class RealmlistUnitOfWork:
    def __init__(self, auth_provider: AuthSessionProvider):
        self.auth_provider = auth_provider
        self.session: AsyncSession | None = None


    async def commit(self) -> None:
        if self.session is None:
            raise RuntimeError("Unit of work is not active")
        await self.session.commit()
    
    async def rollback(self) -> None:
        if self.session is None:
            raise RuntimeError("Unit of work is not active")
        await self.session.rollback()
        
    async def __aenter__(self):
        self.session = self.auth_provider()
        self.realmlists = RealmlistRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.session is None:
            return

        try:
            if exc_type:
                await self.session.rollback()
        finally:
            await self.session.close()